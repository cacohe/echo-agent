import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/repositories/reminder_repository.dart';
import '../../domain/models/reminder.dart';
import 'record_provider.dart';

final reminderRepositoryProvider = Provider<ReminderRepository>((ref) {
  return ReminderRepository(ref.read(dbProvider), ref.read(apiClientProvider));
});

final remindersProvider = FutureProvider<List<Reminder>>((ref) async {
  final repository = ref.read(reminderRepositoryProvider);
  return repository.getReminders();
});