class Reminder {
  final String id;
  final String condition;
  final String action;
  final String? recordId;
  final bool isActive;
  final DateTime? nextTrigger;
  final DateTime createdAt;

  Reminder({
    required this.id,
    required this.condition,
    required this.action,
    this.recordId,
    this.isActive = true,
    this.nextTrigger,
    required this.createdAt,
  });

  factory Reminder.fromJson(Map<String, dynamic> json) {
    return Reminder(
      id: json['id'] as String,
      condition: json['condition'] as String,
      action: json['action'] as String,
      recordId: json['record_id'] as String?,
      isActive: json['is_active'] as bool? ?? true,
      nextTrigger: json['next_trigger'] != null
          ? DateTime.parse(json['next_trigger'] as String)
          : null,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }
}
