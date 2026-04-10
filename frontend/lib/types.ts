export type RecordType = "voice" | "text";

export type Mood = "happy" | "neutral" | "low" | "angry";

export type InsightType = "association" | "pattern" | "counterfactual";

export interface JournalRecord {
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
