# Echo Frontend Design Specification

## Overview

Echo is a personal reflection and decision-making AI assistant. This spec covers the web frontend built with Next.js, designed mobile-first with a clean, modern aesthetic.

**Tech Stack:**
- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS
- IndexedDB (local storage for MVP)
- Framer Motion (animations)

**Design Language:**
- Style: Minimalist modern, inspired by Headspace
- Mobile-first approach
- Soft colors, generous whitespace, card-based layout

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      User Browser                        │
│  ┌─────────────────┐      ┌─────────────────────────┐   │
│  │   Next.js App   │◄────►│   IndexedDB (MVP)      │   │
│  │   (Port 3000)   │      │   Local storage        │   │
│  └────────┬────────┘      └─────────────────────────┘   │
│           │ API Routes (future)                           │
│           ▼                                               │
│  ┌─────────────────┐                                     │
│  │   Backend API   │◄──── Future: Cloud sync             │
│  │   (Port 8000)   │                                     │
│  └─────────────────┘                                     │
└─────────────────────────────────────────────────────────┘
```

---

## Page Structure

### 1. Home Page (`/`)

**Purpose:** Main recording interface and today's overview

**Layout:**
- Top: Greeting + date
- Center: Large microphone button (primary action)
- Below mic: Quick stats (records today, current mood)
- Bottom: Today's insight card (if available)

**Components:**
- `RecordButton` - Large circular mic button with pulse animation
- `QuickStats` - Today's activity summary
- `TodayInsight` - AI insight from recent records
- `VoiceRecorder` - Recording modal with waveform

### 2. History Page (`/history`)

**Purpose:** Browse all past records in chronological order

**Layout:**
- Top: Month selector
- Main: Vertical timeline of records
- Each record card shows: date, preview text, mood tag, insight count

**Components:**
- `Timeline` - Vertical timeline container
- `RecordCard` - Individual record entry
- `MoodTag` - Colored mood indicator
- `SearchBar` - Filter records by keyword
- `DatePicker` - Select month/week

### 3. Insights Page (`/insights`)

**Purpose:** View AI-generated patterns and weekly reports

**Layout:**
- Top: Period selector (This Week / This Month)
- Main: Insight cards in grid
- Sections: Mood trends, Pattern discoveries, Key events

**Components:**
- `WeeklyReport` - Summary card with highlight
- `MoodChart` - Weekly mood distribution visualization
- `PatternCard` - Discovered pattern with confidence
- `TimelineItem` - Key event marker

### 4. Settings Page (`/settings`)

**Purpose:** Configure app preferences

**Layout:**
- Sections: Account, Reminders, Privacy, About
- Toggle switches, selection lists

**Components:**
- `SettingsSection` - Grouped settings
- `ReminderConfig` - Set daily reminder time
- `DataExport` - Export records as JSON
- `PrivacyToggle` - Control data sharing

---

## Core Components

### RecordButton

**States:**
- Default: Purple (#6B5CE7) circle with mic icon
- Hover: Slight scale up (1.05), shadow increase
- Active/Recording: Red (#FF6B6B) with pulse animation, waveform display
- Processing: Spinning loader
- Disabled: Gray, 50% opacity

**Behavior:**
- Tap → Start recording
- Tap again → Stop recording
- Long press → Open text input modal

### InsightCard

**Variants:**
- Association: Purple left border
- Pattern: Orange left border
- Counterfactual: Blue left border

**Structure:**
```
┌────────────────────────────┐
│ [Icon] Title          [X] │
│                            │
│ Content text...            │
│                            │
│ Confidence: 85%     2h ago │
└────────────────────────────┘
```

### MoodTag

**Variants (color-coded):**
- 😊 Happy: Green (#10B981)
- 😐 Neutral: Gray (#6B7280)
- 😔 Low: Orange (#F59E0B)
- 😤 Angry: Red (#FF6B6B)

---

## Data Flow

### Recording a Voice Note

1. User taps mic button
2. Browser requests microphone permission
3. Recording starts, waveform animation plays
4. User taps again to stop
5. Audio sent to speech-to-text (Web Speech API or backend)
6. Text displayed for confirmation
7. User confirms → Saved to IndexedDB
8. If connected to backend → Sync to API

### Fetching Insights

1. App checks for new records since last insight
2. If new records exist → Call backend API
3. API processes records → Returns insights
4. Insights cached locally
5. Display in relevant UI cards

---

## Local Storage (IndexedDB)

**Database:** `echo_db`

**Stores:**

### `records`
```typescript
{
  id: string;
  content: string;
  type: 'voice' | 'text';
  mood?: 'happy' | 'neutral' | 'low' | 'angry';
  created_at: string;
  synced: boolean;
}
```

### `insights`
```typescript
{
  id: string;
  record_id: string;
  type: 'association' | 'pattern' | 'counterfactual';
  content: string;
  confidence: number;
  created_at: string;
}
```

### `reminders`
```typescript
{
  id: string;
  condition: string;
  action: string;
  active: boolean;
  next_trigger?: string;
}
```

---

## API Integration (Future)

When backend is connected:

### `POST /api/records`
Create a new record
```json
Request: { "content": "...", "type": "voice|text", "mood": "happy" }
Response: { "id": "...", "insights": [...] }
```

### `GET /api/records?limit=20&offset=0`
List records
```json
Response: { "records": [...], "total": 100 }
```

### `GET /api/insights/weekly`
Get weekly report
```json
Response: {
  "period": "2024-W15",
  "mood_distribution": { "happy": 5, "low": 3 },
  "patterns": [...],
  "highlight": "..."
}
```

---

## Responsive Breakpoints

| Breakpoint | Width | Behavior |
|------------|-------|----------|
| Mobile | < 640px | Single column, bottom nav |
| Tablet | 640-1024px | Two columns, side nav option |
| Desktop | > 1024px | Three columns, full dashboard |

---

## MVP Scope

**Included:**
- [ ] Home page with record button
- [ ] Voice recording with Web Speech API
- [ ] Text input fallback
- [ ] Record storage in IndexedDB
- [ ] History page with timeline
- [ ] Basic insight display
- [ ] Settings page (reminder config only)

**Excluded (Future):**
- [ ] Backend API integration
- [ ] Cloud sync
- [ ] Push notifications
- [ ] Multi-language support
- [ ] Dark mode

---

## File Structure

```
echo-agent/
├── frontend/                    # Next.js application
│   ├── app/                    # App Router
│   │   ├── page.tsx           # Home page
│   │   ├── history/page.tsx   # History page
│   │   ├── insights/page.tsx  # Insights page
│   │   ├── settings/page.tsx # Settings page
│   │   ├── layout.tsx        # Root layout
│   │   └── globals.css       # Global styles
│   │
│   ├── components/            # React components
│   │   ├── RecordButton.tsx
│   │   ├── InsightCard.tsx
│   │   ├── MoodTag.tsx
│   │   ├── Timeline.tsx
│   │   ├── VoiceRecorder.tsx
│   │   └── ...
│   │
│   ├── lib/                   # Utilities
│   │   ├── db.ts             # IndexedDB operations
│   │   ├── api.ts            # API client
│   │   └── types.ts          # TypeScript types
│   │
│   ├── package.json
│   └── tailwind.config.ts
│
└── src/                       # Backend (existing)
    └── ...
```

---

## Design Tokens

```css
/* Colors */
--primary: #6B5CE7;
--primary-light: #F5F3FF;
--accent: #FF6B6B;
--success: #10B981;
--warning: #F59E0B;
--background: #FAFAFA;
--surface: #FFFFFF;
--text-primary: #1A1A2E;
--text-secondary: #6B7280;

/* Spacing */
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-6: 24px;
--space-8: 32px;

/* Border Radius */
--radius-sm: 8px;
--radius-md: 16px;
--radius-lg: 24px;
--radius-full: 9999px;

/* Shadows */
--shadow-sm: 0 2px 4px rgba(107, 92, 231, 0.08);
--shadow-md: 0 4px 12px rgba(107, 92, 231, 0.12);
--shadow-lg: 0 8px 24px rgba(107, 92, 231, 0.16);
```

---

## Animation Guidelines

- **Page transitions:** Fade + slight slide, 200ms ease-out
- **Card entry:** Fade in + rise, staggered 50ms between items
- **Button press:** Scale to 0.98, 100ms
- **Recording pulse:** Continuous scale 1.0→1.05, 1s ease-in-out
- **Modal:** Fade in backdrop + scale from 0.95→1.0, 300ms
