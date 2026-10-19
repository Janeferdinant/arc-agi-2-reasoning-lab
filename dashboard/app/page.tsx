"use client";

import React, { useState } from "react";
import { Navbar, TabKey } from "../components/Navbar";
import { OverviewTab } from "../components/OverviewTab";
import { DatasetExplorerTab } from "../components/DatasetExplorerTab";
import { ExperimentTrackerTab } from "../components/ExperimentTrackerTab";
import { SolverAnalysisTab } from "../components/SolverAnalysisTab";
import { PlaygroundTab } from "../components/PlaygroundTab";
import { SubmissionCenterTab } from "../components/SubmissionCenterTab";
import { DocumentationTab } from "../components/DocumentationTab";
import { GitBranch, ExternalLink, Terminal } from "lucide-react";

export default function Home() {
  const [activeTab, setActiveTab] = useState<TabKey>("overview");

  return (
    <div className="min-h-screen flex flex-col bg-[#080c14] text-slate-100 selection:bg-cyan-500/20 selection:text-cyan-300">
      {/* Top Navigation */}
      <Navbar activeTab={activeTab} onTabChange={setActiveTab} />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === "overview" && <OverviewTab onNavigate={setActiveTab} />}
        {activeTab === "dataset" && <DatasetExplorerTab />}
        {activeTab === "experiments" && <ExperimentTrackerTab />}
        {activeTab === "solver" && <SolverAnalysisTab />}
        {activeTab === "playground" && <PlaygroundTab />}
        {activeTab === "submission" && <SubmissionCenterTab />}
        {activeTab === "research" && <DocumentationTab />}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-950/70 py-6 mt-12 text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="font-semibold text-slate-200">ARC-AGI-2 Reasoning Lab</span>
            <span>•</span>
            <span>Kaggle ARC Prize 2026 Research Initiative</span>
          </div>

          <div className="flex items-center space-x-6 text-[11px]">
            <a
              href="https://github.com/Janeferdinant/arc-agi-2-reasoning-lab"
              target="_blank"
              rel="noreferrer"
              className="flex items-center space-x-1.5 text-slate-400 hover:text-cyan-400 transition-colors"
            >
              <GitBranch className="w-3.5 h-3.5" />
              <span>GitHub Repository</span>
            </a>
            <a
              href="https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2"
              target="_blank"
              rel="noreferrer"
              className="flex items-center space-x-1.5 text-slate-400 hover:text-cyan-400 transition-colors"
            >
              <span>Kaggle Competition</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
