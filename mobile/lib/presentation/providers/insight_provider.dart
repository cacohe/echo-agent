import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/repositories/insight_repository.dart';
import '../../domain/models/insight.dart';
import 'record_provider.dart';

final insightRepositoryProvider = Provider<InsightRepository>((ref) {
  return InsightRepository(ref.read(dbProvider), ref.read(apiClientProvider));
});

final insightsProvider = FutureProvider<List<Insight>>((ref) async {
  final repository = ref.read(insightRepositoryProvider);
  return repository.getInsights();
});