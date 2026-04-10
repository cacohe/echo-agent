import 'package:flutter/material.dart';
import '../../core/theme.dart';
import '../../domain/models/record.dart';
import '../../domain/models/enums.dart';

class QuickStats extends StatelessWidget {
  final List<Record> records;

  const QuickStats({super.key, required this.records});

  @override
  Widget build(BuildContext context) {
    final todayCount = records.length;
    final moodCounts = <Mood, int>{};
    for (final r in records) {
      if (r.mood != null) {
        moodCounts[r.mood!] = (moodCounts[r.mood!] ?? 0) + 1;
      }
    }

    Mood? dominantMood;
    if (moodCounts.isNotEmpty) {
      dominantMood = moodCounts.entries.reduce((a, b) => a.value > b.value ? a : b).key;
    }

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppTheme.surface,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: AppTheme.primary.withOpacity(0.08),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _StatItem(label: '今日记录', value: todayCount.toString()),
          if (dominantMood != null)
            _StatItem(label: '主导情绪', value: _moodLabel(dominantMood)),
        ],
      ),
    );
  }

  String _moodLabel(Mood mood) {
    switch (mood) {
      case Mood.happy:
        return '开心';
      case Mood.neutral:
        return '平静';
      case Mood.low:
        return '低落';
      case Mood.angry:
        return '愤怒';
    }
  }
}

class _StatItem extends StatelessWidget {
  final String label;
  final String value;

  const _StatItem({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          value,
          style: const TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: AppTheme.primary,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: const TextStyle(
            fontSize: 12,
            color: AppTheme.textSecondary,
          ),
        ),
      ],
    );
  }
}
