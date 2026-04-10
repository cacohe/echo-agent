import 'package:flutter/material.dart';
import '../../core/constants.dart';
import '../../domain/models/enums.dart';

class MoodChip extends StatelessWidget {
  final Mood mood;
  final bool showLabel;

  const MoodChip({
    super.key,
    required this.mood,
    this.showLabel = true,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: Color(AppConstants.moodColors[mood.name] ?? 0xFF6B7280).withOpacity(0.1),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            AppConstants.moodEmojis[mood.name] ?? '',
            style: const TextStyle(fontSize: 16),
          ),
          if (showLabel) ...[
            const SizedBox(width: 4),
            Text(
              _moodLabel(mood),
              style: TextStyle(
                color: Color(AppConstants.moodColors[mood.name] ?? 0xFF6B7280),
                fontSize: 14,
              ),
            ),
          ],
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
