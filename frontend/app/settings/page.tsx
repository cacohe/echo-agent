"use client";

import { useState } from "react";
import { getAllRecords, getAllInsights } from "@/lib/db";

export default function SettingsPage() {
  const [exportStatus, setExportStatus] = useState<string>("");

  const handleExport = async () => {
    try {
      const records = await getAllRecords();
      const insights = await getAllInsights();
      const data = { records, insights, exported_at: new Date().toISOString() };
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `echo-export-${new Date().toISOString().split("T")[0]}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      setExportStatus("导出成功");
    } catch {
      setExportStatus("导出失败");
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="p-6 pb-4">
        <h1 className="text-2xl font-semibold text-text-primary">设置</h1>
      </header>

      <main className="px-4 space-y-6">
        <section className="bg-surface rounded-lg p-4 shadow-sm">
          <h2 className="text-sm font-medium text-text-secondary mb-3">数据管理</h2>
          <button
            onClick={handleExport}
            className="w-full px-4 py-2 bg-primary text-white rounded-lg"
          >
            导出所有数据
          </button>
          {exportStatus && (
            <p className="mt-2 text-sm text-success">{exportStatus}</p>
          )}
        </section>

        <section className="bg-surface rounded-lg p-4 shadow-sm">
          <h2 className="text-sm font-medium text-text-secondary mb-3">关于</h2>
          <div className="space-y-2 text-sm">
            <p className="text-text-primary">Echo v0.1.0</p>
            <p className="text-text-secondary">个人复盘与决策AI助手</p>
          </div>
        </section>
      </main>
    </div>
  );
}