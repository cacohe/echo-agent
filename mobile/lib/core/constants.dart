class AppConstants {
  static const String appName = 'Echo';
  static const String apiBaseUrl = 'http://localhost:8000';
  
  static const Map<String, String> moodEmojis = {
    'happy': '😊',
    'neutral': '😐',
    'low': '😔',
    'angry': '😤',
  };
  
  static const Map<String, int> moodColors = {
    'happy': 0xFF10B981,
    'neutral': 0xFF6B7280,
    'low': 0xFFF59E0B,
    'angry': 0xFFFF6B6B,
  };
}
