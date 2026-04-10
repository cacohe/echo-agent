import 'package:dio/dio.dart';
import '../../domain/models/insight.dart';
import '../local/database_helper.dart';
import '../remote/api_client.dart';

class InsightRepository {
  final DatabaseHelper _db;
  final ApiClient _api;

  InsightRepository(this._db, this._api);

  Future<List<Insight>> getInsights() async {
    try {
      final response = await _api.get('/api/insights/weekly');
      if (response.statusCode == 200) {
        final Map<String, dynamic> data = response.data;
        // Weekly report might have insights embedded
        // Handle accordingly
        return [];
      }
    } on DioError {
      // Fallback to local
    }
    return _db.getInsights();
  }

  Future<void> saveInsight(Insight insight) async {
    await _db.insertInsight(insight);
  }
}