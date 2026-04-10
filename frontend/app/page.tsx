"use client";

import { useEffect, useState } from "react";
import { RecordButton } from "@/components/RecordButton";
import { QuickStats } from "@/components/QuickStats";
import { TodayInsight } from "@/components/TodayInsight";
import { getRecentRecords } from "@/lib/db";
import type { JournalRecord } from "@/lib/types";

export default function HomePage() {
  const [todayRecords, setTodayRecords] = useState<JournalRecord[]>([]);

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