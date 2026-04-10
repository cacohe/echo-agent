import type { Metadata } from "next";
import "./globals.css";
import { BottomNav } from "@/components/BottomNav";

export const metadata: Metadata = {
  title: "Echo - Personal Reflection AI",
  description: "Your daily reflection and decision companion",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen bg-background">
        <main className="pb-20">{children}</main>
        <BottomNav />
      </body>
    </html>
  );
}