"use client";

import React from "react";
import {
  BrainCircuit,
  Database,
  BarChart3,
  Microscope,
  Gamepad2,
  FileCheck2,
  BookOpen,
  ExternalLink,
} from "lucide-react";

export type TabKey =
  | "overview"
  | "dataset"
  | "experiments"
  | "solver"
  | "playground"
  | "submission"
  | "research";

interface NavbarProps {
  activeTab: TabKey;
  onTabChange: (tab: TabKey) => void;
}

export function Navbar({ activeTab, onTabChange }: NavbarProps) {
  const tabs: { key: TabKey; label: string; icon: React.ReactNode }[] = [
    { key: "overview", label: "Overview", icon: <BrainCircuit className="w-4 h-4" /> },
    { key: "dataset", label: "Dataset Explorer", icon: <Database className="w-4 h-4" /> },
    { key: "experiments", label: "Experiments", icon: <BarChart3 className="w-4 h-4" /> },
    { key: "solver", label: "Solver Analysis", icon: <Microscope className="w-4 h-4" /> },
    { key: "playground", label: "Playground", icon: <Gamepad2 className="w-4 h-4" /> },
    { key: "submission", label: "Submission", icon: <FileCheck2 className="w-4 h-4" /> },
    { key: "research", label: "Research Docs", icon: <BookOpen className="w-4 h-4" /> },
  ];

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Title */}
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <BrainCircuit className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-base tracking-tight text-white">
                  ARC-AGI-2 Reasoning Lab
                </span>
                <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-cyan-950/80 text-cyan-400 border border-cyan-800/60">
                  Prize 2026
                </span>
              </div>
              <p className="text-[11px] text-slate-400">
                Official Benchmark Solver & Empirical Evaluation Dashboard
              </p>
            </div>
          </div>

          {/* Quick status pill */}
          <div className="hidden lg:flex items-center space-x-3 text-xs">
            <span className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-emerald-950/60 text-emerald-400 border border-emerald-800/50">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              <span>Offline Verified • Pass@2 Active</span>
            </span>
            <a
              href="https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2"
              target="_blank"
              rel="noreferrer"
              className="flex items-center space-x-1 text-slate-400 hover:text-cyan-400 transition-colors"
            >
              <span>Kaggle Competition</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex space-x-1 overflow-x-auto pb-2 scrollbar-none">
          {tabs.map((tab) => {
            const isActive = activeTab === tab.key;
            return (
              <button
                key={tab.key}
                onClick={() => onTabChange(tab.key)}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-xs font-medium transition-all whitespace-nowrap ${
                  isActive
                    ? "bg-cyan-500/15 text-cyan-400 border border-cyan-500/30 shadow-sm shadow-cyan-500/10"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 border border-transparent"
                }`}
              >
                {tab.icon}
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
