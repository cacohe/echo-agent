import 'package:dio/dio.dart';
import 'package:uuid/uuid.dart';
import '../../domain/models/record.dart';
import '../../domain/models/enums.dart';
import '../local/database_helper.dart';
import '../remote/api_client.dart';

class RecordRepository {
  final DatabaseHelper _db;
  final ApiClient _api;
  final _uuid = const Uuid();

  RecordRepository(this._db, this._api);

  Future<Record> createRecord({
    required String content,
    required RecordType type,
    Mood? mood,
    Map<String, dynamic>? context,
  }) async {
    final record = Record(
      id: _uuid.v4(),
      content: content,
      type: type,
      mood: mood,
      createdAt: DateTime.now(),
      context: context,
      synced: false,
    );

    await _db.insertRecord(record);

    try {
      final response = await _api.post('/api/records', data: record.toJson());
      if (response.statusCode == 201) {
        await _db.markRecordSynced(record.id);
        return record.copyWith(synced: true);
      }
    } on DioError {
      // Offline - record saved locally, will sync later
    }

    return record;
  }

  Future<List<Record>> getRecords({int limit = 50, int offset = 0}) async {
    try {
      final response = await _api.get('/api/records', queryParameters: {
        'limit': limit,
        'offset': offset,
      });
      if (response.statusCode == 200) {
        final List<dynamic> data = response.data;
        return data.map((json) => Record.fromJson(json)).toList();
      }
    } on DioError {
      // Fallback to local
    }
    return _db.getRecords(limit: limit, offset: offset);
  }

  Future<void> deleteRecord(String id) async {
    await _db.deleteRecord(id);
    try {
      await _api.delete('/api/records/$id');
    } on DioError {
      // Ignore remote errors
    }
  }

  Future<List<Record>> getUnsyncedRecords() async {
    return _db.getUnsyncedRecords();
  }

  Future<void> markSynced(String id) async {
    await _db.markRecordSynced(id);
  }
}