"use client";

import { useEffect, useState } from "react";
import { TimelineItem } from "./TimelineItem";
import { EmptyState } from "./EmptyState";
import { getAllRecords } from "@/lib/db";
import type { JournalRecord } from "@/lib/types";

interface TimelineProps {
  onSelectRecord?: (record: JournalRecord) => void;
}

export function Timeline({ onSelectRecord }: TimelineProps) {
  const [records, setRecords] = useState<JournalRecord[]>([]);
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