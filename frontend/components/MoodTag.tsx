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