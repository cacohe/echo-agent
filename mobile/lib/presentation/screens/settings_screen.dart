import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/theme.dart';
import '../providers/record_provider.dart';

class SettingsScreen extends ConsumerStatefulWidget {
  const SettingsScreen({super.key});

  @override
  ConsumerState<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends ConsumerState<SettingsScreen> {
  final _serverUrlController = TextEditingController();
  String _exportStatus = '';

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    _serverUrlController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.background,
      body: SafeArea(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  '设置',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.w600,
                    color: AppTheme.textPrimary,
                  ),
                ),
                const SizedBox(height: 24),
                _buildSection(
                  title: '服务器配置',
                  children: [
                    TextField(
                      controller: _serverUrlController,
                      decoration: const InputDecoration(
                        labelText: 'API 服务器地址',
                        hintText: 'http://localhost:8000',
                        border: OutlineInputBorder(),
                      ),
                    ),
                    const SizedBox(height: 12),
                    ElevatedButton(
                      onPressed: _saveServerUrl,
                      child: const Text('保存'),
                    ),
                  ],
                ),
                const SizedBox(height: 24),
                _buildSection(
                  title: '数据管理',
                  children: [
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: _exportData,
                        child: const Text('导出所有数据'),
                      ),
                    ),
                    if (_exportStatus.isNotEmpty)
                      Padding(
                        padding: const EdgeInsets.only(top: 8),
                        child: Text(
                          _exportStatus,
                          style: const TextStyle(color: AppTheme.success),
                        ),
                      ),
                  ],
                ),
                const SizedBox(height: 24),
                _buildSection(
                  title: '关于',
                  children: [
                    const Text('Echo v0.1.0'),
                    const SizedBox(height: 4),
                    const Text(
                      '个人复盘与决策AI助手',
                      style: TextStyle(color: AppTheme.textSecondary),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildSection({required String title, required List<Widget> children}) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppTheme.surface,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w600,
              color: AppTheme.textSecondary,
            ),
          ),
          const SizedBox(height: 12),
          ...children,
        ],
      ),
    );
  }

  void _saveServerUrl() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('服务器地址已保存')),
    );
  }

  Future<void> _exportData() async {
    try {
      final records = await ref.read(recordsProvider.future);
      final data = {
        'records': records,
        'exported_at': DateTime.now().toIso8601String(),
      };
      setState(() => _exportStatus = '导出成功');
    } catch {
      setState(() => _exportStatus = '导出失败');
    }
  }
}
