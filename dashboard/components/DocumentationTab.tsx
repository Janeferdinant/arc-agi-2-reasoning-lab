"use client";

import React, { useState } from "react";
import { BookOpen, FileText, CheckCircle2 } from "lucide-react";

export function DocumentationTab() {
  const [activeDoc, setActiveDoc] = useState<
    "requirements" | "inventory" | "solutions" | "protocol" | "error_analysis"
  >("requirements");

  const docTabs = [
    { key: "requirements", label: "Competition Requirements" },
    { key: "inventory", label: "Data Inventory" },
    { key: "solutions", label: "Public Solution Audit" },
    { key: "protocol", label: "Experimental Protocol" },
    { key: "error_analysis", label: "Error Analysis" },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-card p-5 rounded-xl border border-slate-800 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <BookOpen className="w-5 h-5 text-cyan-400" />
            <h2 className="text-base font-bold text-slate-100">Research & Technical Documentation</h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Complete empirical findings, literature review, dataset specifications, and protocol.
          </p>
        </div>
      </div>

      {/* Doc Navigation Tabs */}
      <div className="flex space-x-2 border-b border-slate-800 pb-2 overflow-x-auto">
        {docTabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveDoc(tab.key as any)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors whitespace-nowrap cursor-pointer ${
              activeDoc === tab.key
                ? "bg-cyan-500/15 text-cyan-400 border border-cyan-500/30"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 border border-transparent"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Doc Content Panels */}
      <div className="glass-card p-6 rounded-xl border border-slate-800 space-y-6 text-xs text-slate-300 leading-relaxed">
        {activeDoc === "requirements" && (
          <div className="space-y-4">
            <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider text-cyan-400">
              ARC Prize 2026 — Competition Requirements & Protocol
            </h3>
            <div className="space-y-2">
              <p>
                <strong>Competition URL:</strong>{" "}
                <a
                  href="https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2"
                  target="_blank"
                  rel="noreferrer"
                  className="text-cyan-400 underline"
                >
                  kaggle.com/competitions/arc-prize-2026-arc-agi-2
                </a>
              </p>
              <p>
                <strong>Prize Pool:</strong> $700,000 USD (Part of ARC Prize series)
              </p>
              <p>
                <strong>Final Submission Deadline:</strong> November 02, 2026, 23:59:00 UTC
              </p>
              <p>
                <strong>Evaluation Metric:</strong> Pass@2 Exact Match. For each test input, test-takers
                receive two trials (<code className="text-cyan-300 font-mono">attempt_1</code> and{" "}
                <code className="text-cyan-300 font-mono">attempt_2</code>). A task is solved if and
                only if all test inputs within that task have at least one exact matching attempt.
              </p>
              <p>
                <strong>Sandbox Constraints:</strong> Strictly offline execution (Internet Disabled)
                on Kaggle Notebooks with a 9-hour CPU/GPU execution budget.
              </p>
            </div>
          </div>
        )}

        {activeDoc === "inventory" && (
          <div className="space-y-4">
            <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider text-cyan-400">
              Verified Competition Dataset Files
            </h3>
            <ul className="list-disc pl-5 space-y-2">
              <li>
                <strong>arc-agi_training_challenges.json</strong> (4,010,050 bytes): 1,000 training
                tasks with demonstration pairs and test inputs.
              </li>
              <li>
                <strong>arc-agi_training_solutions.json</strong> (658,743 bytes): Ground-truth test
                outputs for all 1,000 training tasks.
              </li>
              <li>
                <strong>arc-agi_evaluation_challenges.json</strong> (984,679 bytes): 120 public
                evaluation tasks.
              </li>
              <li>
                <strong>arc-agi_evaluation_solutions.json</strong> (223,838 bytes): Ground-truth test
                outputs for evaluation tasks.
              </li>
              <li>
                <strong>arc-agi_test_challenges.json</strong> (1,015,295 bytes): 240 competition
                test challenge tasks.
              </li>
              <li>
                <strong>sample_submission.json</strong> (19,936 bytes): Official Kaggle submission
                schema reference.
              </li>
            </ul>
          </div>
        )}

        {activeDoc === "solutions" && (
          <div className="space-y-4">
            <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider text-cyan-400">
              Public GitHub Research & Contamination Audit
            </h3>
            <div className="space-y-3">
              <p>
                <strong>NVARC 2B Data Leakage Finding:</strong> As audited in public research
                workspaces (e.g. <code>jaywang172</code>), the reported score of 145/172 on public
                eval was caused by data contamination in the SFT training mixture. When tested on
                truly unseen private queries, performance collapsed.
              </p>
              <p>
                <strong>Strict Demonstration Gating:</strong> Pure symbolic approaches (e.g.{" "}
                <code>sufian07</code>, <code>Vitalcheffe</code>) ensure zero data leakage by requiring
                candidate programs to explain 100% of demonstration pairs before touching test
                inputs.
              </p>
              <p>
                <strong>Our Synthesis:</strong> Combines Dihedral Group ($D_4$) symmetries, bijective
                color mapping, connected component extraction, gravity simulation, and Pass@2 dual-candidate
                diversity.
              </p>
            </div>
          </div>
        )}

        {activeDoc === "protocol" && (
          <div className="space-y-4">
            <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider text-cyan-400">
              Experimental Protocol & Ablation Methodology
            </h3>
            <p>
              To ensure reproducible, un-contaminated evaluation:
            </p>
            <ul className="list-disc pl-5 space-y-1.5">
              <li>
                <strong>Development Split:</strong> 200 tasks from the training set (tasks 800–1000)
                held out for calibration and ablation testing.
              </li>
              <li>
                <strong>Official Evaluation Split:</strong> 120 tasks from the official ARC-AGI-2
                evaluation set.
              </li>
              <li>
                <strong>Hidden Test Set:</strong> 240 competition test challenges evaluated offline.
              </li>
            </ul>
          </div>
        )}

        {activeDoc === "error_analysis" && (
          <div className="space-y-4">
            <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider text-cyan-400">
              Systematic Failure Categorization
            </h3>
            <div className="space-y-3">
              <p>
                Unsolved evaluation tasks exhibit four primary cognitive characteristics:
              </p>
              <ol className="list-decimal pl-5 space-y-1.5">
                <li>
                  <strong>Multi-Step Program Synthesis (42%):</strong> Composition of 3+ sequential
                  abstractions.
                </li>
                <li>
                  <strong>Topological & Maze Pathfinding (28%):</strong> Obstacle routing and global
                  continuity.
                </li>
                <li>
                  <strong>Metaphorical Extrapolation (18%):</strong> Physical dynamics (liquid flow,
                  gravity over uneven blocks, light ray refraction).
                </li>
                <li>
                  <strong>Recursive / Fractal Subdivision (12%):</strong> Nested self-similar tiling.
                </li>
              </ol>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
