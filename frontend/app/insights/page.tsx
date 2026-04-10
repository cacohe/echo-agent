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