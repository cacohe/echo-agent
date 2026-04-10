import 'enums.dart';

class Insight {
  final String id;
  final String recordId;
  final InsightType type;
  final String content;
  final double confidence;
  final DateTime createdAt;
  final List<String> relatedRecordIds;

  Insight({
    required this.id,
    required this.recordId,
    required this.type,
    required this.content,
    required this.confidence,
    required this.createdAt,
    this.relatedRecordIds = const [],
  });

  factory Insight.fromJson(Map<String, dynamic> json) {
    return Insight(
      id: json['id'] as String,
      recordId: json['record_id'] as String,
      type: InsightType.values.byName(json['type'] as String),
      content: json['content'] as String,
      confidence: (json['confidence'] as num).toDouble(),
      createdAt: DateTime.parse(json['created_at'] as String),
      relatedRecordIds: (json['related_record_ids'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          [],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'record_id': recordId,
      'type': type.name,
      'content': content,
      'confidence': confidence,
      'created_at': createdAt.toIso8601String(),
      'related_record_ids': relatedRecordIds,
    };
  }
}
