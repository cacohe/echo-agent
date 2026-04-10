"use client";

import type { JournalRecord } from "@/lib/types";

interface QuickStatsProps {
  records: JournalRecord[];
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