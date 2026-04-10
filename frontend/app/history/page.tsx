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