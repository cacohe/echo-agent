# Echo Mobile App Design

## 1. Overview

Implement a native Flutter mobile app (iOS/Android) that shares the same backend as the existing web frontend. The app provides voice/text recording, AI insights, pattern recognition, and proactive reminders.

## 2. Architecture

### Pattern: Riverpod + Repository

```
┌─────────────────────────────────────┐
│         Flutter Mobile App          │
├─────────────────────────────────────┤
│  Presentation Layer                 │
│  - Screens (Home, History, Insights, │
│    Settings)                        │
│  - Widgets (shared components)      │
├─────────────────────────────────────┤
│  State Management (Riverpod)       │
│  - recordProvider                  │
│  - insightProvider                 │
│  - reminderProvider                │
│  - syncProvider                    │
├─────────────────────────────────────┤
│  Repository Layer                  │
│  - RecordRepository                │
│  - InsightRepository               │
│  - ReminderRepository              │
├─────────────────────────────────────┤
│  Data Sources                      │
│  - Local: SQLite (sqflite)         │
│  - Remote: REST API (dio)           │
│  - Sync Manager                   │
└─────────────────────────────────────┘
```

### Project Structure

```
mobile/                         # Flutter app root
├── lib/
│   ├── main.dart
│   ├── app.dart
│   │
│   ├── core/
│   │   ├── constants.dart       # API URLs, colors, moods
│   │   ├── theme.dart           # App theme
│   │   └── utils.dart           # Date formatting, etc.
│   │
│   ├── data/
│   │   ├── local/
│   │   │   └── database_helper.dart  # SQLite operations
│   │   ├── remote/
│   │   │   └── api_client.dart      # Dio HTTP client
│   │   └── repositories/
│   │       ├── record_repository.dart
│   │       ├── insight_repository.dart
│   │       └── reminder_repository.dart
│   │
│   ├── domain/
│   │   └── models/
│   │       ├── record.dart
│   │       ├── insight.dart
│   │       └── reminder.dart
│   │
│   ├── presentation/
│   │   ├── providers/
│   │   │   ├── record_provider.dart
│   │   │   ├── insight_provider.dart
│   │   │   ├── reminder_provider.dart
│   │   │   └── sync_provider.dart
│   │   │
│   │   ├── screens/
│   │   │   ├── home_screen.dart
│   │   │   ├── history_screen.dart
│   │   │   ├── insights_screen.dart
│   │   │   └── settings_screen.dart
│   │   │
│   │   └── widgets/
│   │       ├── record_button.dart
│   │       ├── mood_chip.dart
│   │       ├── insight_card.dart
│   │       ├── timeline_item.dart
│   │       └── bottom_nav.dart
│   │
│   └── services/
│       ├── audio_service.dart       # Voice recording
│       ├── notification_service.dart # Local notifications
│       └── sync_service.dart        # Offline sync
│
├── pubspec.yaml
└── android/ ios/                    # Native platform files
```

## 3. Backend API (Shared)

The mobile app uses the same REST API as the web frontend:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/records` | POST | Create new record |
| `/api/records` | GET | List records |
| `/api/records/{id}` | GET | Get single record |
| `/api/insights/weekly` | GET | Weekly report |
| `/api/insights/reminders` | GET | Get reminders |
| `/api/insights/reminders` | POST | Create reminder |

### API Base URL

- Default: `http://localhost:8000`
- Configurable via app settings

## 4. Data Models

### Record
```dart
class Record {
  final String id;
  final String content;
  final RecordType type;  // voice, text
  final Mood? mood;
  final DateTime createdAt;
  final Map<String, dynamic>? context;
  final bool synced;
}
```

### Insight
```dart
class Insight {
  final String id;
  final String recordId;
  final InsightType type;  // association, pattern, counterfactual
  final String content;
  final double confidence;
  final DateTime createdAt;
}
```

### Reminder
```dart
class Reminder {
  final String id;
  final String condition;
  final String action;
  final String? recordId;
  final bool isActive;
  final DateTime? nextTrigger;
  final DateTime createdAt;
}
```

## 5. Core Features

### 5.1 Voice Recording
- Use `record` package for cross-platform audio recording
- Recording states: idle, recording, processing
- WAV format for best quality
- After recording: send to backend or transcribe locally

### 5.2 Offline Support
- Local SQLite storage via `sqflite`
- All records saved locally first (optimistic UI)
- `connectivity_plus` monitors network state
- When online: sync pending records to backend
- Conflict resolution: server timestamp wins

### 5.3 Push Notifications
- `flutter_local_notifications` for local notifications
- `firebase_messaging` for FCM (optional, requires Firebase setup)
- Scheduled notifications via workmanager

### 5.4 Sync Flow
```
1. User creates record
2. Save to local SQLite (synced=false)
3. If online → POST to backend
4. On success → update synced=true
5. If offline → queue for later sync
6. On reconnect → sync all pending records
```

## 6. Screens

### HomeScreen
- Large record button (center)
- Today's mood summary
- Recent insight preview
- Bottom navigation

### HistoryScreen
- Timeline list of records
- Pull-to-refresh
- Filter by mood

### InsightsScreen
- Weekly report card
- List of insights (association, pattern)
- Empty state for no data

### SettingsScreen
- API server URL configuration
- Data export (JSON)
- Notification preferences
- App version info

## 7. Dependencies

```yaml
dependencies:
  flutter_riverpod: ^2.4.0
  riverpod_annotation: ^2.3.0
  dio: ^5.4.0
  sqflite: ^2.3.0
  path_provider: ^2.1.0
  record: ^5.0.0
  flutter_local_notifications: ^16.0.0
  connectivity_plus: ^5.0.0
  uuid: ^4.0.0
  intl: ^0.18.0

dev_dependencies:
  build_runner
  riverpod_generator
```

## 8. Implementation Phases

### Phase 1: Project Setup
- [ ] Initialize Flutter project
- [ ] Configure dependencies
- [ ] Set up theme and constants
- [ ] Verify build on iOS/Android

### Phase 2: Data Layer
- [ ] SQLite database helper
- [ ] API client with Dio
- [ ] Repository implementations
- [ ] Offline queue logic

### Phase 3: State Management
- [ ] Riverpod providers
- [ ] Sync provider
- [ ] Connection status monitoring

### Phase 4: UI Implementation
- [ ] HomeScreen with RecordButton
- [ ] HistoryScreen with TimelineList
- [ ] InsightsScreen
- [ ] SettingsScreen with server config
- [ ] Bottom navigation

### Phase 5: Native Features
- [ ] Voice recording service
- [ ] Local notifications
- [ ] Background sync (optional)

## 9. Notes

- Voice transcription happens on backend (same as web)
- API URL stored locally for flexibility
- All timestamps in UTC, displayed in local timezone
