"use client";

import Link from "next/link";

const navItems = [
  { href: "/", label: "首页" },
  { href: "/history", label: "历史" },
  { href: "/insights", label: "洞察" },
  { href: "/settings", label: "设置" },
];

export function BottomNav() {
  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-surface border-t border-gray-200 px-4 py-2 z-40">
      <div className="flex justify-around items-center max-w-md mx-auto">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="flex flex-col items-center py-1 px-3 text-text-secondary hover:text-primary"
          >
            <span className="text-xs">{item.label}</span>
          </Link>
        ))}
      </div>
    </nav>
  );
}