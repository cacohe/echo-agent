import 'package:connectivity_plus/connectivity_plus.dart';
import '../data/local/database_helper.dart';
import '../data/remote/api_client.dart';
import '../data/repositories/record_repository.dart';

class SyncService {
  final DatabaseHelper _db;
  final ApiClient _api;
  final RecordRepository _recordRepository;

  SyncService(this._db, this._api, this._recordRepository);

  Future<void> syncPendingRecords() async {
    final connectivity = await Connectivity().checkConnectivity();
    if (connectivity.contains(ConnectivityResult.none)) {
      return;
    }

    final unsyncedRecords = await _recordRepository.getUnsyncedRecords();
    
    for (final record in unsyncedRecords) {
      try {
        await _api.post('/api/records', data: record.toJson());
        await _recordRepository.markSynced(record.id);
      } catch (e) {
        // Will retry on next sync
        break;
      }
    }
  }

  Stream<List<ConnectivityResult>> watchConnectivity() {
    return Connectivity().onConnectivityChanged;
  }
}
