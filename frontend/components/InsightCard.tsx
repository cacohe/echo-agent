import { formatRelativeTime } from "@/lib/utils";
import type { Insight } from "@/lib/types";

interface InsightCardProps {
  insight: Insight;
}

const typeLabels = {
  association: "关联洞察",
  pattern: "模式发现",
  counterfactual: "反事实推演",
};

const borderColors = {
  association: "border-l-primary",
  pattern: "border-l-warning",
  counterfactual: "border-l-blue-500",
};

export function InsightCard({ insight }: InsightCardProps) {
  return (
    <div className={`bg-surface rounded-lg p-4 shadow-sm border-l-4 ${borderColors[insight.type]}`}>
      <div className="flex justify-between items-start mb-2">
        <span className="text-xs font-medium text-primary bg-primary-light px-2 py-0.5 rounded">
          {typeLabels[insight.type]}
        </span>
        <span className="text-xs text-text-secondary">
          {formatRelativeTime(insight.created_at)}
        </span>
      </div>
      <p className="text-text-primary text-sm">{insight.content}</p>
      <div className="mt-2 flex items-center gap-2">
        <span className="text-xs text-text-secondary">
          置信度: {Math.round(insight.confidence * 100)}%
        </span>
      </div>
    </div>
  );
}