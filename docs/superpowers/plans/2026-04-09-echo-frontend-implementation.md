# Echo Frontend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Echo web frontend with Next.js - a mobile-first personal reflection app with voice/text recording and local storage.

**Architecture:** Next.js 14 App Router, TypeScript, Tailwind CSS, IndexedDB for local storage. Frontend runs on port 3000, connects to backend API on port 8000 for AI features.

**Tech Stack:** Next.js 14+, TypeScript, Tailwind CSS, Framer Motion, idb (IndexedDB wrapper), Web Speech API

---

## File Structure

```
echo-agent/
├── frontend/                    # Next.js application
│   ├── app/                    # App Router
│   │   ├── page.tsx           # Home page
│   │   ├── history/page.tsx   # History page
│   │   ├── insights/page.tsx   # Insights page
│   │   ├── settings/page.tsx   # Settings page
│   │   ├── layout.tsx         # Root layout with nav
│   │   └── globals.css         # Global styles + Tailwind
│   │
│   ├── components/             # React components
│   │   ├── RecordButton.tsx   # Main voice record button
│   │   ├── VoiceRecorder.tsx  # Recording modal
│   │   ├── InsightCard.tsx    # Insight display card
│   │   ├── MoodTag.tsx        # Mood indicator tag
│   │   ├── Timeline.tsx        # Record timeline
│   │   ├── TimelineItem.tsx    # Individual timeline entry
│   │   ├── QuickStats.tsx     # Today's stats
│   │   ├── TodayInsight.tsx    # Today's AI insight
│   │   ├── BottomNav.tsx       # Mobile bottom navigation
│   │   ├── Header.tsx          # Page header
│   │   └── EmptyState.tsx      # Empty state placeholder
│   │
│   ├── lib/                    # Utilities
│   │   ├── db.ts              # IndexedDB operations
│   │   ├── types.ts            # TypeScript types
│   │   ├── utils.ts            # Helper functions
│   │   └── constants.ts         # App constants
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── postcss.config.js
│
└── src/                        # Backend (existing)
    └── ...
```

---

## Task 1: Project Setup

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/tsconfig.json`
- Create: `frontend/tailwind.config.ts`
- Create: `frontend/next.config.js`
- Create: `frontend/postcss.config.js`
- Create: `frontend/app/globals.css`
- Create: `frontend/app/layout.tsx`

- [ ] **Step 1: Create frontend/package.json**

```json
{
  "name": "echo-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "next": "14.2.3",
    "framer-motion": "^11.1.7",
    "idb": "^8.0.0"
  },
  "devDependencies": {
    "typescript": "^5.4.5",
    "@types/node": "^20.12.7",
    "@types/react": "^18.3.1",
    "@types/react-dom": "^18.3.0",
    "tailwindcss": "^3.4.3",
    "postcss": "^8.4.38",
    "autoprefixer": "^10.4.19",
    "eslint": "^8.57.0",
    "eslint-config-next": "14.2.3"
  }
}
```

- [ ] **Step 2: Create frontend/tsconfig.json**

```json
{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{"name": "next"}],
    "paths": {"@/*": ["./*"]}
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

- [ ] **Step 3: Create frontend/tailwind.config.ts**

```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#6B5CE7",
          light: "#F5F3FF",
        },
        accent: "#FF6B6B",
        success: "#10B981",
        warning: "#F59E0B",
        background: "#FAFAFA",
        surface: "#FFFFFF",
        "text-primary": "#1A1A2E",
        "text-secondary": "#6B7280",
      },
      borderRadius: {
        sm: "8px",
        md: "16px",
        lg: "24px",
      },
      boxShadow: {
        sm: "0 2px 4px rgba(107, 92, 231, 0.08)",
        md: "0 4px 12px rgba(107, 92, 231, 0.12)",
        lg: "0 8px 24px rgba(107, 92, 231, 0.16)",
      },
    },
  },
  plugins: [],
};
export default config;
```

- [ ] **Step 4: Create frontend/next.config.js**

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
};

module.exports = nextConfig;
```

- [ ] **Step 5: Create frontend/postcss.config.js**

```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

- [ ] **Step 6: Create frontend/app/globals.css**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --primary: #6B5CE7;
  --primary-light: #F5F3FF;
  --accent: #FF6B6B;
  --success: #10B981;
  --warning: #F59E0B;
  --background: #FAFAFA;
  --surface: #FFFFFF;
  --text-primary: #1A1A2E;
  --text-secondary: #6B7280;
}

html,
body {
  max-width: 100vw;
  overflow-x: hidden;
  background-color: var(--background);
  color: var(--text-primary);
}

* {
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}

a {
  color: inherit;
  text-decoration: none;
}
```

- [ ] **Step 7: Create frontend/app/layout.tsx**

```tsx
import type { Metadata } from "next";
import "./globals.css";
import { BottomNav } from "@/components/BottomNav";

export const metadata: Metadata = {
  title: "Echo - Personal Reflection AI",
  description: "Your daily reflection and decision companion",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen bg-background">
        <main className="pb-20">{children}</main>
        <BottomNav />
      </body>
    </html>
  );
}
```

- [ ] **Step 8: Install dependencies**

```bash
cd frontend && npm install
```

- [ ] **Step 9: Commit**

```bash
git add frontend/package.json frontend/tsconfig.json frontend/tailwind.config.ts frontend/next.config.js frontend/postcss.config.js frontend/app/globals.css frontend/app/layout.tsx
git commit -m "feat(frontend): scaffold Next.js project with Tailwind"
```

---

## Task 2: Types and Constants

**Files:**
- Create: `frontend/lib/types.ts`
- Create: `frontend/lib/constants.ts`
- Create: `frontend/lib/utils.ts`

- [ ] **Step 1: Create frontend/lib/types.ts**

```typescript
export type RecordType = "voice" | "text";

export type Mood = "happy" | "neutral" | "low" | "angry";

export type InsightType = "association" | "pattern" | "counterfactual";

export interface Record {
  id: string;
  content: string;
  type: RecordType;
  mood?: Mood;
  created_at: string;
  synced: boolean;
}

export interface Insight {
  id: string;
  record_id: string;
  type: InsightType;
  content: string;
  confidence: number;
  created_at: string;
}

export interface Reminder {
  id: string;
  condition: string;
  action: string;
  active: boolean;
  next_trigger?: string;
}

export interface WeeklyReport {
  period: string;
  total_records: number;
  mood_distribution: Record<string, number>;
  patterns: PatternInfo[];
  highlight: string;
}

export interface PatternInfo {
  name: string;
  description: string;
  frequency: number;
  confidence: number;
}
```

- [ ] **Step 2: Create frontend/lib/constants.ts**

```typescript
export const APP_NAME = "Echo";

export const MOOD_EMOJIS: Record<string, string> = {
  happy: "😊",
  neutral: "😐",
  low: "😔",
  angry: "😤",
};

export const MOOD_COLORS: Record<string, string> = {
  happy: "bg-success",
  neutral: "bg-text-secondary",
  low: "bg-warning",
  angry: "bg-accent",
};

export const INSIGHT_COLORS: Record<string, string> = {
  association: "border-l-primary",
  pattern: "border-l-warning",
  counterfactual: "border-l-blue-500",
};

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
```

- [ ] **Step 3: Create frontend/lib/utils.ts**

```typescript
import { type ClassValue, clsx } from "clsx";

export function cn(...inputs: ClassValue[]) {
  return inputs.filter(Boolean).join(" ");
}

export function formatDate(date: string | Date): string {
  const d = typeof date === "string" ? new Date(date) : date;
  return d.toLocaleDateString("zh-CN", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function formatRelativeTime(date: string | Date): string {
  const d = typeof date === "string" ? new Date(date) : date;
  const now = new Date();
  const diff = now.getTime() - d.getTime();
  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (days > 7) return formatDate(d);
  if (days > 0) return `${days}天前`;
  if (hours > 0) return `${hours}小时前`;
  if (minutes > 0) return `${minutes}分钟前`;
  return "刚刚";
}

export function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}
```

- [ ] **Step 4: Commit**

```bash
git add frontend/lib/types.ts frontend/lib/constants.ts frontend/lib/utils.ts
git commit -m "feat(frontend): add TypeScript types and utilities"
```

---

## Task 3: IndexedDB Database Layer

**Files:**
- Create: `frontend/lib/db.ts`

- [ ] **Step 1: Create frontend/lib/db.ts**

```typescript
import { openDB, DBSchema, IDBPDatabase } from "idb";
import type { Record, Insight, Reminder } from "./types";

interface EchoDB extends DBSchema {
  records: {
    key: string;
    value: Record;
    indexes: { "by-date": string };
  };
  insights: {
    key: string;
    value: Insight;
    indexes: { "by-record": string };
  };
  reminders: {
    key: string;
    value: Reminder;
  };
}

const DB_NAME = "echo_db";
const DB_VERSION = 1;

let dbPromise: Promise<IDBPDatabase<EchoDB>> | null = null;

export function getDB(): Promise<IDBPDatabase<EchoDB>> {
  if (!dbPromise) {
    dbPromise = openDB<EchoDB>(DB_NAME, DB_VERSION, {
      upgrade(db) {
        if (!db.objectStoreNames.contains("records")) {
          const recordStore = db.createObjectStore("records", { keyPath: "id" });
          recordStore.createIndex("by-date", "created_at");
        }
        if (!db.objectStoreNames.contains("insights")) {
          const insightStore = db.createObjectStore("insights", { keyPath: "id" });
          insightStore.createIndex("by-record", "record_id");
        }
        if (!db.objectStoreNames.contains("reminders")) {
          db.createObjectStore("reminders", { keyPath: "id" });
        }
      },
    });
  }
  return dbPromise;
}

export async function addRecord(record: Record): Promise<void> {
  const db = await getDB();
  await db.add("records", record);
}

export async function getRecord(id: string): Promise<Record | undefined> {
  const db = await getDB();
  return db.get("records", id);
}

export async function getAllRecords(): Promise<Record[]> {
  const db = await getDB();
  const records = await db.getAllFromIndex("records", "by-date");
  return records.reverse();
}

export async function getRecentRecords(limit: number = 20): Promise<Record[]> {
  const db = await getDB();
  const records = await db.getAllFromIndex("records", "by-date");
  return records.reverse().slice(0, limit);
}

export async function deleteRecord(id: string): Promise<void> {
  const db = await getDB();
  await db.delete("records", id);
}

export async function addInsight(insight: Insight): Promise<void> {
  const db = await getDB();
  await db.add("insights", insight);
}

export async function getInsightsByRecord(recordId: string): Promise<Insight[]> {
  const db = await getDB();
  return db.getAllFromIndex("insights", "by-record", recordId);
}

export async function getAllInsights(): Promise<Insight[]> {
  const db = await getDB();
  return db.getAll("insights");
}

export async function addReminder(reminder: Reminder): Promise<void> {
  const db = await getDB();
  await db.add("reminders", reminder);
}

export async function getActiveReminders(): Promise<Reminder[]> {
  const db = await getDB();
  const all = await db.getAll("reminders");
  return all.filter((r) => r.active);
}

export async function updateReminder(reminder: Reminder): Promise<void> {
  const db = await getDB();
  await db.put("reminders", reminder);
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/lib/db.ts
git commit -m "feat(frontend): add IndexedDB database layer"
```

---

## Task 4: Core Components - RecordButton

**Files:**
- Create: `frontend/components/RecordButton.tsx`

- [ ] **Step 1: Create frontend/components/RecordButton.tsx**

```tsx
"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { VoiceRecorder } from "./VoiceRecorder";

export function RecordButton() {
  const [isRecording, setIsRecording] = useState(false);
  const [showRecorder, setShowRecorder] = useState(false);

  const handleStartRecording = () => {
    setIsRecording(true);
    setShowRecorder(true);
  };

  const handleStopRecording = () => {
    setIsRecording(false);
  };

  const handleClose = () => {
    setShowRecorder(false);
    setIsRecording(false);
  };

  return (
    <>
      <motion.button
        onClick={handleStartRecording}
        className="w-32 h-32 rounded-full bg-primary shadow-lg flex items-center justify-center"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <svg
          className="w-12 h-12 text-white"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
          />
        </svg>
      </motion.button>

      {showRecorder && (
        <VoiceRecorder
          onClose={handleClose}
          onStop={handleStopRecording}
        />
      )}
    </>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/components/RecordButton.tsx
git commit -m "feat(frontend): add RecordButton component"
```

---

## Task 5: Core Components - VoiceRecorder

**Files:**
- Create: `frontend/components/VoiceRecorder.tsx`

- [ ] **Step 1: Create frontend/components/VoiceRecorder.tsx**

```tsx
"use client";

import { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { addRecord } from "@/lib/db";
import { generateId } from "@/lib/utils";

interface VoiceRecorderProps {
  onClose: () => void;
  onStop: () => void;
}

export function VoiceRecorder({ onClose, onStop }: VoiceRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [duration, setDuration] = useState(0);
  const [transcript, setTranscript] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined" && ("SpeechRecognition" in window || "webkitSpeechRecognition" in window)) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = true;
      recognitionRef.current.lang = "zh-CN";

      recognitionRef.current.onresult = (event) => {
        let finalTranscript = "";
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          }
        }
        if (finalTranscript) {
          setTranscript((prev) => prev + finalTranscript);
        }
      };

      recognitionRef.current.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
      };
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  const startRecording = () => {
    if (recognitionRef.current) {
      recognitionRef.current.start();
    }
    setIsRecording(true);
    timerRef.current = setInterval(() => {
      setDuration((d) => d + 1);
    }, 1000);
  };

  const stopRecording = async () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }
    setIsRecording(false);
    setIsProcessing(true);

    const text = transcript || "语音记录";
    const record = {
      id: generateId(),
      content: text,
      type: "voice" as const,
      created_at: new Date().toISOString(),
      synced: false,
    };

    await addRecord(record);

    setIsProcessing(false);
    onStop();
    onClose();
  };

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.95 }}
        animate={{ scale: 1 }}
        className="bg-surface rounded-lg p-6 m-4 max-w-sm w-full"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold text-text-primary">录音中</h2>
          <button onClick={onClose} className="text-text-secondary">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="flex flex-col items-center">
          <motion.div
            animate={isRecording ? { scale: [1, 1.1, 1] } : {}}
            transition={{ repeat: Infinity, duration: 1 }}
            className={`w-20 h-20 rounded-full ${isRecording ? "bg-accent" : "bg-primary"} flex items-center justify-center mb-4`}
          >
            <svg className="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
              <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
            </svg>
          </motion.div>

          <p className="text-2xl font-mono mb-4">{formatDuration(duration)}</p>

          {transcript && (
            <div className="w-full bg-primary-light rounded-lg p-3 mb-4 max-h-32 overflow-y-auto">
              <p className="text-sm text-text-primary">{transcript}</p>
            </div>
          )}

          <div className="flex gap-4">
            {!isRecording ? (
              <motion.button
                whileTap={{ scale: 0.95 }}
                onClick={startRecording}
                className="px-6 py-2 bg-primary text-white rounded-full"
              >
                开始录音
              </motion.button>
            ) : (
              <motion.button
                whileTap={{ scale: 0.95 }}
                onClick={stopRecording}
                disabled={isProcessing}
                className="px-6 py-2 bg-accent text-white rounded-full disabled:opacity-50"
              >
                {isProcessing ? "处理中..." : "停止"}
              </motion.button>
            )}
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/components/VoiceRecorder.tsx
git commit -m "feat(frontend): add VoiceRecorder modal with speech recognition"
```

---

## Task 6: Home Page

**Files:**
- Create: `frontend/app/page.tsx`
- Modify: `frontend/components/BottomNav.tsx` (create first)

- [ ] **Step 1: Create frontend/components/BottomNav.tsx**

```tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/", label: "首页", icon: "home" },
  { href: "/history", label: "历史", icon: "clock" },
  { href: "/insights", label: "洞察", icon: "chart" },
  { href: "/settings", label: "设置", icon: "cog" },
];

export function BottomNav() {
  const pathname = usePathname();

  const icons: Record<string, JSX.Element> = {
    home: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
      </svg>
    ),
    clock: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
    chart: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
    ),
    cog: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    ),
  };

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-surface border-t border-gray-200 px-4 py-2 z-40">
      <div className="flex justify-around items-center max-w-md mx-auto">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex flex-col items-center py-1 px-3 rounded-lg transition-colors ${
                isActive ? "text-primary" : "text-text-secondary"
              }`}
            >
              {icons[item.icon]}
              <span className="text-xs mt-1">{item.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
```

- [ ] **Step 2: Create frontend/app/page.tsx**

```tsx
"use client";

import { useEffect, useState } from "react";
import { RecordButton } from "@/components/RecordButton";
import { QuickStats } from "@/components/QuickStats";
import { TodayInsight } from "@/components/TodayInsight";
import { getRecentRecords } from "@/lib/db";
import type { Record } from "@/lib/types";

export default function HomePage() {
  const [todayRecords, setTodayRecords] = useState<Record[]>([]);

  useEffect(() => {
    loadTodayRecords();
  }, []);

  const loadTodayRecords = async () => {
    const records = await getRecentRecords(50);
    const today = new Date().toDateString();
    const todayRecs = records.filter(
      (r) => new Date(r.created_at).toDateString() === today
    );
    setTodayRecords(todayRecs);
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <header className="p-6">
        <h1 className="text-2xl font-semibold text-text-primary">你好</h1>
        <p className="text-text-secondary">
          {new Date().toLocaleDateString("zh-CN", {
            weekday: "long",
            month: "long",
            day: "numeric",
          })}
        </p>
      </header>

      <section className="flex-1 flex flex-col items-center justify-center px-4">
        <RecordButton />
        <p className="mt-6 text-text-secondary text-sm">点击录音，说出你的想法</p>
      </section>

      <section className="px-4 pb-4">
        <QuickStats records={todayRecords} />
        <TodayInsight records={todayRecords} />
      </section>
    </div>
  );
}
```

- [ ] **Step 3: Create frontend/components/QuickStats.tsx**

```tsx
"use client";

import type { Record } from "@/lib/types";

interface QuickStatsProps {
  records: Record[];
}

export function QuickStats({ records }: QuickStatsProps) {
  return (
    <div className="grid grid-cols-2 gap-3 mb-4">
      <div className="bg-surface rounded-lg p-4 shadow-sm">
        <p className="text-text-secondary text-sm">今日记录</p>
        <p className="text-2xl font-semibold text-text-primary">{records.length}</p>
      </div>
      <div className="bg-surface rounded-lg p-4 shadow-sm">
        <p className="text-text-secondary text-sm">本周记录</p>
        <p className="text-2xl font-semibold text-text-primary">-</p>
      </div>
    </div>
  );
}
```

- [ ] **Step 4: Create frontend/components/TodayInsight.tsx**

```tsx
"use client";

import type { Record } from "@/lib/types";

interface TodayInsightProps {
  records: Record[];
}

export function TodayInsight({ records }: TodayInsightProps) {
  if (records.length === 0) {
    return null;
  }

  const lastRecord = records[records.length - 1];

  return (
    <div className="bg-primary-light rounded-lg p-4 shadow-sm">
      <h3 className="text-sm font-medium text-primary mb-2">今日洞察</h3>
      <p className="text-text-primary text-sm">
        {lastRecord.type === "voice" ? "你录了一段语音" : "你记录了一条想法"}
      </p>
    </div>
  );
}
```

- [ ] **Step 5: Commit**

```bash
git add frontend/app/page.tsx frontend/components/BottomNav.tsx frontend/components/QuickStats.tsx frontend/components/TodayInsight.tsx
git commit -m "feat(frontend): add home page with record button and stats"
```

---

## Task 7: History Page

**Files:**
- Create: `frontend/app/history/page.tsx`
- Create: `frontend/components/Timeline.tsx`
- Create: `frontend/components/TimelineItem.tsx`
- Create: `frontend/components/MoodTag.tsx`

- [ ] **Step 1: Create frontend/components/MoodTag.tsx**

```tsx
import { MOOD_EMOJIS } from "@/lib/constants";
import type { Mood } from "@/lib/types";

interface MoodTagProps {
  mood?: Mood;
  size?: "sm" | "md";
}

const moodColors = {
  happy: "bg-success/20 text-success",
  neutral: "bg-gray-200 text-text-secondary",
  low: "bg-warning/20 text-warning",
  angry: "bg-accent/20 text-accent",
};

export function MoodTag({ mood, size = "sm" }: MoodTagProps) {
  if (!mood) return null;

  const sizeClasses = size === "sm" ? "px-2 py-0.5 text-xs" : "px-3 py-1 text-sm";

  return (
    <span className={`inline-flex items-center gap-1 rounded-full ${moodColors[mood]} ${sizeClasses}`}>
      <span>{MOOD_EMOJIS[mood]}</span>
      <span>{mood === "low" ? "低落" : mood === "angry" ? "愤怒" : mood}</span>
    </span>
  );
}
```

- [ ] **Step 2: Create frontend/components/TimelineItem.tsx**

```tsx
import { formatRelativeTime } from "@/lib/utils";
import { MoodTag } from "./MoodTag";
import type { Record } from "@/lib/types";

interface TimelineItemProps {
  record: Record;
  onClick?: () => void;
}

export function TimelineItem({ record, onClick }: TimelineItemProps) {
  return (
    <div
      onClick={onClick}
      className="bg-surface rounded-lg p-4 shadow-sm mb-3 cursor-pointer hover:shadow-md transition-shadow"
    >
      <div className="flex justify-between items-start mb-2">
        <span className="text-xs text-text-secondary">
          {formatRelativeTime(record.created_at)}
        </span>
        <MoodTag mood={record.mood} />
      </div>
      <p className="text-text-primary text-sm line-clamp-2">{record.content}</p>
      {record.type === "voice" && (
        <div className="flex items-center gap-1 mt-2 text-primary text-xs">
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
          </svg>
          <span>语音</span>
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 3: Create frontend/components/Timeline.tsx**

```tsx
"use client";

import { useEffect, useState } from "react";
import { TimelineItem } from "./TimelineItem";
import { EmptyState } from "./EmptyState";
import { getAllRecords } from "@/lib/db";
import type { Record } from "@/lib/types";

interface TimelineProps {
  onSelectRecord?: (record: Record) => void;
}

export function Timeline({ onSelectRecord }: TimelineProps) {
  const [records, setRecords] = useState<Record[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRecords();
  }, []);

  const loadRecords = async () => {
    setLoading(true);
    const allRecords = await getAllRecords();
    setRecords(allRecords);
    setLoading(false);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (records.length === 0) {
    return <EmptyState message="还没有记录" />;
  }

  return (
    <div className="space-y-1">
      {records.map((record) => (
        <TimelineItem
          key={record.id}
          record={record}
          onClick={() => onSelectRecord?.(record)}
        />
      ))}
    </div>
  );
}
```

- [ ] **Step 4: Create frontend/components/EmptyState.tsx**

```tsx
interface EmptyStateProps {
  message?: string;
}

export function EmptyState({ message = "暂无数据" }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="w-16 h-16 bg-primary-light rounded-full flex items-center justify-center mb-4">
        <svg className="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
        </svg>
      </div>
      <p className="text-text-secondary">{message}</p>
    </div>
  );
}
```

- [ ] **Step 5: Create frontend/app/history/page.tsx**

```tsx
"use client";

import { Timeline } from "@/components/Timeline";

export default function HistoryPage() {
  return (
    <div className="min-h-screen bg-background">
      <header className="p-6 pb-4">
        <h1 className="text-2xl font-semibold text-text-primary">历史记录</h1>
        <p className="text-text-secondary text-sm">回顾你的每一次记录</p>
      </header>

      <main className="px-4">
        <Timeline />
      </main>
    </div>
  );
}
```

- [ ] **Step 6: Commit**

```bash
git add frontend/app/history/page.tsx frontend/components/Timeline.tsx frontend/components/TimelineItem.tsx frontend/components/MoodTag.tsx frontend/components/EmptyState.tsx
git commit -m "feat(frontend): add history page with timeline"
```

---

## Task 8: Insights Page

**Files:**
- Create: `frontend/app/insights/page.tsx`
- Create: `frontend/components/InsightCard.tsx`

- [ ] **Step 1: Create frontend/components/InsightCard.tsx**

```tsx
import { formatRelativeTime } from "@/lib/utils";
import type { Insight } from "@/lib/types";

interface InsightCardProps {
  insight: Insight;
}

const typeLabels = {
  association: "关联洞察",
  pattern: "模式发现",
  counterfactual: "反事实推演",
};

const borderColors = {
  association: "border-l-primary",
  pattern: "border-l-warning",
  counterfactual: "border-l-blue-500",
};

export function InsightCard({ insight }: InsightCardProps) {
  return (
    <div className={`bg-surface rounded-lg p-4 shadow-sm border-l-4 ${borderColors[insight.type]}`}>
      <div className="flex justify-between items-start mb-2">
        <span className="text-xs font-medium text-primary bg-primary-light px-2 py-0.5 rounded">
          {typeLabels[insight.type]}
        </span>
        <span className="text-xs text-text-secondary">
          {formatRelativeTime(insight.created_at)}
        </span>
      </div>
      <p className="text-text-primary text-sm">{insight.content}</p>
      <div className="mt-2 flex items-center gap-2">
        <span className="text-xs text-text-secondary">
          置信度: {Math.round(insight.confidence * 100)}%
        </span>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Create frontend/app/insights/page.tsx**

```tsx
"use client";

import { InsightCard } from "@/components/InsightCard";
import { EmptyState } from "@/components/EmptyState";
import { getAllInsights } from "@/lib/db";
import type { Insight } from "@/lib/types";
import { useEffect, useState } from "react";

export default function InsightsPage() {
  const [insights, setInsights] = useState<Insight[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadInsights();
  }, []);

  const loadInsights = async () => {
    setLoading(true);
    const allInsights = await getAllInsights();
    setInsights(allInsights);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="p-6 pb-4">
        <h1 className="text-2xl font-semibold text-text-primary">洞察</h1>
        <p className="text-text-secondary text-sm">发现你的情绪和行为模式</p>
      </header>

      <main className="px-4">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
        ) : insights.length === 0 ? (
          <EmptyState message="还没有洞察，继续记录吧" />
        ) : (
          <div className="space-y-4">
            {insights.map((insight) => (
              <InsightCard key={insight.id} insight={insight} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
```

- [ ] **Step 3: Commit**

```bash
git add frontend/app/insights/page.tsx frontend/components/InsightCard.tsx
git commit -m "feat(frontend): add insights page"
```

---

## Task 9: Settings Page

**Files:**
- Create: `frontend/app/settings/page.tsx`

- [ ] **Step 1: Create frontend/app/settings/page.tsx**

```tsx
"use client";

import { useState } from "react";
import { getAllRecords, getAllInsights } from "@/lib/db";

export default function SettingsPage() {
  const [exportStatus, setExportStatus] = useState<string>("");

  const handleExport = async () => {
    try {
      const records = await getAllRecords();
      const insights = await getAllInsights();
      const data = { records, insights, exported_at: new Date().toISOString() };
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `echo-export-${new Date().toISOString().split("T")[0]}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      setExportStatus("导出成功");
    } catch {
      setExportStatus("导出失败");
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="p-6 pb-4">
        <h1 className="text-2xl font-semibold text-text-primary">设置</h1>
      </header>

      <main className="px-4 space-y-6">
        <section className="bg-surface rounded-lg p-4 shadow-sm">
          <h2 className="text-sm font-medium text-text-secondary mb-3">数据管理</h2>
          <button
            onClick={handleExport}
            className="w-full px-4 py-2 bg-primary text-white rounded-lg"
          >
            导出所有数据
          </button>
          {exportStatus && (
            <p className="mt-2 text-sm text-success">{exportStatus}</p>
          )}
        </section>

        <section className="bg-surface rounded-lg p-4 shadow-sm">
          <h2 className="text-sm font-medium text-text-secondary mb-3">关于</h2>
          <div className="space-y-2 text-sm">
            <p className="text-text-primary">Echo v0.1.0</p>
            <p className="text-text-secondary">个人复盘与决策AI助手</p>
          </div>
        </section>
      </main>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/app/settings/page.tsx
git commit -m "feat(frontend): add settings page with data export"
```

---

## Task 10: Test and Verify

- [ ] **Step 1: Build the application**

```bash
cd frontend && npm run build
```

Expected: Build completes without errors

- [ ] **Step 2: Start development server**

```bash
cd frontend && npm run dev &
sleep 5
curl -s http://localhost:3000 | head -50
```

Expected: HTML page with "Echo" title

- [ ] **Step 3: Verify pages**

Open browser and check:
- `/` - Home page with record button
- `/history` - History page with timeline
- `/insights` - Insights page
- `/settings` - Settings page

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat(frontend): complete Echo web application"
```

---

## Plan Summary

| Task | Description |
|------|-------------|
| 1 | Project Setup - Next.js with Tailwind |
| 2 | Types and Constants |
| 3 | IndexedDB Database Layer |
| 4 | RecordButton Component |
| 5 | VoiceRecorder with Speech Recognition |
| 6 | Home Page with Stats |
| 7 | History Page with Timeline |
| 8 | Insights Page |
| 9 | Settings Page |
| 10 | Test and Verify |

---

## Execution Options

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**