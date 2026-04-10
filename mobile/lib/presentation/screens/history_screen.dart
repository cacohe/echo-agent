import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/theme.dart';
import '../providers/record_provider.dart';
import '../widgets/timeline_item.dart';

class HistoryScreen extends ConsumerWidget {
  const HistoryScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final recordsAsync = ref.watch(recordsProvider);

    return Scaffold(
      backgroundColor: AppTheme.background,
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Padding(
              padding: EdgeInsets.all(24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '历史记录',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.w600,
                      color: AppTheme.textPrimary,
                    ),
                  ),
                  SizedBox(height: 4),
                  Text(
                    '回顾你的每一次记录',
                    style: TextStyle(color: AppTheme.textSecondary),
                  ),
                ],
              ),
            ),
            Expanded(
              child: recordsAsync.when(
                data: (records) {
                  if (records.isEmpty) {
                    return const Center(
                      child: Text(
                        '还没有记录，开始录音吧',
                        style: TextStyle(color: AppTheme.textSecondary),
                      ),
                    );
                  }
                  return RefreshIndicator(
                    onRefresh: () async {
                      ref.read(recordsProvider.notifier).loadRecords();
                    },
                    child: ListView.builder(
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      itemCount: records.length,
                      itemBuilder: (context, index) {
                        final record = records[index];
                        return TimelineItem(
                          record: record,
                          onDelete: () {
                            ref.read(recordsProvider.notifier).deleteRecord(record.id);
                          },
                        );
                      },
                    ),
                  );
                },
                loading: () => const Center(child: CircularProgressIndicator()),
                error: (error, _) => Center(child: Text('Error: $error')),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
