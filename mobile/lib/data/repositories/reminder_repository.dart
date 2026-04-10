import 'package:dio/dio.dart';
import 'package:uuid/uuid.dart';
import '../../domain/models/reminder.dart';
import '../local/database_helper.dart';
import '../remote/api_client.dart';

class ReminderRepository {
  final DatabaseHelper _db;
  final ApiClient _api;
  final _uuid = const Uuid();

  ReminderRepository(this._db, this._api);

  Future<List<Reminder>> getReminders() async {
    try {
      final response = await _api.get('/api/insights/reminders');
      if (response.statusCode == 200) {
        final List<dynamic> data = response.data;
        return data.map((json) => Reminder.fromJson(json)).toList();
      }
    } on DioError {
      // Fallback to local
    }
    return _db.getActiveReminders();
  }

  Future<Reminder> createReminder({
    required String condition,
    required String action,
    String? recordId,
  }) async {
    final reminder = Reminder(
      id: _uuid.v4(),
      condition: condition,
      action: action,
      recordId: recordId,
      createdAt: DateTime.now(),
    );

    await _db.insertReminder(reminder);

    try {
      await _api.post('/api/insights/reminders', data: {
        'condition': condition,
        'action': action,
        'record_id': recordId,
      });
    } on DioError {
      // Offline - reminder saved locally
    }

    return reminder;
  }
}