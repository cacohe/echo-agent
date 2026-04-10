import 'enums.dart';

class Record {
  final String id;
  final String content;
  final RecordType type;
  final Mood? mood;
  final DateTime createdAt;
  final Map<String, dynamic>? context;
  final bool synced;

  Record({
    required this.id,
    required this.content,
    required this.type,
    this.mood,
    required this.createdAt,
    this.context,
    this.synced = false,
  });

  factory Record.fromJson(Map<String, dynamic> json) {
    return Record(
      id: json['id'] as String,
      content: json['content'] as String,
      type: RecordType.values.byName(json['type'] as String),
      mood: json['mood'] != null ? Mood.values.byName(json['mood'] as String) : null,
      createdAt: DateTime.parse(json['created_at'] as String),
      context: json['context'] as Map<String, dynamic>?,
      synced: true,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'content': content,
      'type': type.name,
      'mood': mood?.name,
      'created_at': createdAt.toIso8601String(),
      'context': context,
    };
  }

  Record copyWith({bool? synced}) {
    return Record(
      id: id,
      content: content,
      type: type,
      mood: mood,
      createdAt: createdAt,
      context: context,
      synced: synced ?? this.synced,
    );
  }
}
