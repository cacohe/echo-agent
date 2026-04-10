import { formatRelativeTime } from "@/lib/utils";
import { MoodTag } from "./MoodTag";
import type { JournalRecord } from "@/lib/types";

interface TimelineItemProps {
  record: JournalRecord;
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