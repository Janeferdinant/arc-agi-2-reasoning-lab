import React from "react";
import "./globals.css";

export const metadata = {
  title: "ARC Prize 2026 — ARC-AGI-2 Reasoning Lab",
  description: "Autonomous reasoning engine, empirical ablation benchmarking, and interactive ARC-AGI-2 task playground.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark h-full antialiased">
      <body className="min-h-full flex flex-col bg-[#080c14] text-slate-100">
        {children}
      </body>
    </html>
  );
}
