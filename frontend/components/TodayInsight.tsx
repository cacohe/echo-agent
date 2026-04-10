"use client";

import type { JournalRecord } from "@/lib/types";

interface TodayInsightProps {
  records: JournalRecord[];
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