import 'package:flutter/material.dart';
import '../../core/theme.dart';
import '../../core/utils.dart' as utils;
import '../../domain/models/insight.dart';
import '../../domain/models/enums.dart';

class InsightCard extends StatelessWidget {
  final Insight insight;

  const InsightCard({super.key, required this.insight});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      decoration: BoxDecoration(
        color: AppTheme.surface,
        borderRadius: BorderRadius.circular(16),
        border: Border(
          left: BorderSide(
            color: _typeColor(insight.type),
            width: 4,
          ),
        ),
        boxShadow: [
          BoxShadow(
            color: AppTheme.primary.withOpacity(0.08),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(_typeIcon(insight.type), size: 20, color: _typeColor(insight.type)),
                const SizedBox(width: 8),
                Text(
                  _typeLabel(insight.type),
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                    color: _typeColor(insight.type),
                  ),
                ),
                const Spacer(),
                Text(
                  utils.DateUtils.formatRelative(insight.createdAt),
                  style: const TextStyle(
                    fontSize: 12,
                    color: AppTheme.textSecondary,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              insight.content,
              style: const TextStyle(
                fontSize: 14,
                color: AppTheme.textPrimary,
                height: 1.5,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Color _typeColor(InsightType type) {
    switch (type) {
      case InsightType.association:
        return AppTheme.primary;
      case InsightType.pattern:
        return AppTheme.warning;
      case InsightType.counterfactual:
        return Colors.blue;
    }
  }

  IconData _typeIcon(InsightType type) {
    switch (type) {
      case InsightType.association:
        return Icons.link;
      case InsightType.pattern:
        return Icons.timeline;
      case InsightType.counterfactual:
        return Icons.help_outline;
    }
  }

  String _typeLabel(InsightType type) {
    switch (type) {
      case InsightType.association:
        return '关联洞察';
      case InsightType.pattern:
        return '模式发现';
      case InsightType.counterfactual:
        return '反事实推演';
    }
  }
}
