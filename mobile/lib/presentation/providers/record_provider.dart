import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/local/database_helper.dart';
import '../../data/remote/api_client.dart';
import '../../data/repositories/record_repository.dart';
import '../../domain/models/record.dart';
import '../../domain/models/enums.dart';

final dbProvider = Provider<DatabaseHelper>((ref) => DatabaseHelper());
final apiClientProvider = Provider<ApiClient>((ref) => ApiClient());
final recordRepositoryProvider = Provider<RecordRepository>((ref) {
  return RecordRepository(ref.read(dbProvider), ref.read(apiClientProvider));
});

final recordsProvider = StateNotifierProvider<RecordsNotifier, AsyncValue<List<Record>>>((ref) {
  return RecordsNotifier(ref.read(recordRepositoryProvider));
});

class RecordsNotifier extends StateNotifier<AsyncValue<List<Record>>> {
  final RecordRepository _repository;

  RecordsNotifier(this._repository) : super(const AsyncValue.loading()) {
    loadRecords();
  }

  Future<void> loadRecords() async {
    state = const AsyncValue.loading();
    try {
      final records = await _repository.getRecords();
      state = AsyncValue.data(records);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<Record> createRecord({
    required String content,
    required RecordType type,
    Mood? mood,
  }) async {
    final record = await _repository.createRecord(
      content: content,
      type: type,
      mood: mood,
    );

    state.whenData((records) {
      state = AsyncValue.data([record, ...records]);
    });

    return record;
  }

  Future<void> deleteRecord(String id) async {
    await _repository.deleteRecord(id);
    state.whenData((records) {
      state = AsyncValue.data(records.where((r) => r.id != id).toList());
    });
  }
}