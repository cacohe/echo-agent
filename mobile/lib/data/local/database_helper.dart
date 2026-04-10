import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import '../../domain/models/record.dart';
import '../../domain/models/insight.dart';
import '../../domain/models/reminder.dart';

class DatabaseHelper {
  static Database? _database;

  Future<Database> get database async {
    _database ??= await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, 'echo.db');

    return openDatabase(
      path,
      version: 1,
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE records (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            type TEXT NOT NULL,
            mood TEXT,
            created_at TEXT NOT NULL,
            context TEXT,
            synced INTEGER DEFAULT 0
          )
        ''');
        await db.execute('''
          CREATE TABLE insights (
            id TEXT PRIMARY KEY,
            record_id TEXT NOT NULL,
            type TEXT NOT NULL,
            content TEXT NOT NULL,
            confidence REAL NOT NULL,
            created_at TEXT NOT NULL,
            related_record_ids TEXT
          )
        ''');
        await db.execute('''
          CREATE TABLE reminders (
            id TEXT PRIMARY KEY,
            condition TEXT NOT NULL,
            action TEXT NOT NULL,
            record_id TEXT,
            is_active INTEGER DEFAULT 1,
            next_trigger TEXT,
            created_at TEXT NOT NULL
          )
        ''');
      },
    );
  }

  // Record operations
  Future<void> insertRecord(Record record) async {
    final db = await database;
    await db.insert('records', {
      'id': record.id,
      'content': record.content,
      'type': record.type.name,
      'mood': record.mood?.name,
      'created_at': record.createdAt.toIso8601String(),
      'context': record.context?.toString(),
      'synced': record.synced ? 1 : 0,
    });
  }

  Future<List<Record>> getRecords({int limit = 50, int offset = 0}) async {
    final db = await database;
    final maps = await db.query(
      'records',
      orderBy: 'created_at DESC',
      limit: limit,
      offset: offset,
    );
    return maps.map((m) => _recordFromMap(m)).toList();
  }

  Future<List<Record>> getUnsyncedRecords() async {
    final db = await database;
    final maps = await db.query('records', where: 'synced = ?', whereArgs: [0]);
    return maps.map((m) => _recordFromMap(m)).toList();
  }

  Future<void> markRecordSynced(String id) async {
    final db = await database;
    await db.update('records', {'synced': 1}, where: 'id = ?', whereArgs: [id]);
  }

  Future<void> deleteRecord(String id) async {
    final db = await database;
    await db.delete('records', where: 'id = ?', whereArgs: [id]);
  }

  Record _recordFromMap(Map<String, dynamic> map) {
    return Record(
      id: map['id'] as String,
      content: map['content'] as String,
      type: RecordType.values.byName(map['type'] as String),
      mood: map['mood'] != null ? Mood.values.byName(map['mood'] as String) : null,
      createdAt: DateTime.parse(map['created_at'] as String),
      synced: (map['synced'] as int) == 1,
    );
  }

  // Insight operations
  Future<void> insertInsight(Insight insight) async {
    final db = await database;
    await db.insert('insights', {
      'id': insight.id,
      'record_id': insight.recordId,
      'type': insight.type.name,
      'content': insight.content,
      'confidence': insight.confidence,
      'created_at': insight.createdAt.toIso8601String(),
      'related_record_ids': insight.relatedRecordIds.join(','),
    });
  }

  Future<List<Insight>> getInsights() async {
    final db = await database;
    final maps = await db.query('insights', orderBy: 'created_at DESC');
    return maps.map((m) => _insightFromMap(m)).toList();
  }

  Insight _insightFromMap(Map<String, dynamic> map) {
    return Insight(
      id: map['id'] as String,
      recordId: map['record_id'] as String,
      type: InsightType.values.byName(map['type'] as String),
      content: map['content'] as String,
      confidence: (map['confidence'] as num).toDouble(),
      createdAt: DateTime.parse(map['created_at'] as String),
      relatedRecordIds: (map['related_record_ids'] as String?)?.split(',') ?? [],
    );
  }

  // Reminder operations
  Future<List<Reminder>> getActiveReminders() async {
    final db = await database;
    final maps = await db.query('reminders', where: 'is_active = ?', whereArgs: [1]);
    return maps.map((m) => _reminderFromMap(m)).toList();
  }

  Future<void> insertReminder(Reminder reminder) async {
    final db = await database;
    await db.insert('reminders', {
      'id': reminder.id,
      'condition': reminder.condition,
      'action': reminder.action,
      'record_id': reminder.recordId,
      'is_active': reminder.isActive ? 1 : 0,
      'next_trigger': reminder.nextTrigger?.toIso8601String(),
      'created_at': reminder.createdAt.toIso8601String(),
    });
  }

  Reminder _reminderFromMap(Map<String, dynamic> map) {
    return Reminder(
      id: map['id'] as String,
      condition: map['condition'] as String,
      action: map['action'] as String,
      recordId: map['record_id'] as String?,
      isActive: (map['is_active'] as int) == 1,
      nextTrigger: map['next_trigger'] != null
          ? DateTime.parse(map['next_trigger'] as String)
          : null,
      createdAt: DateTime.parse(map['created_at'] as String),
    );
  }
}
