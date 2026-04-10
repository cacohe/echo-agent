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
