"use client";

import React from "react";
import {
  Trophy,
  CheckCircle2,
  FileCheck,
  Zap,
  Layers,
  ArrowUpRight,
  ShieldCheck,
  Cpu,
  Clock,
  Sparkles,
} from "lucide-react";
import experimentsData from "../data/experiments.json";
import qualityReport from "../data/data_quality_report.json";

export function OverviewTab({ onNavigate }: { onNavigate: (tab: any) => void }) {
  const bestExp = experimentsData[experimentsData.length - 1];

  return (
    <div className="space-y-6">
      {/* Top Banner / Hero */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900/90 to-cyan-950/40 border border-cyan-800/30 p-6 md:p-8 shadow-2xl">
        <div className="relative z-10 max-w-3xl">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-mono mb-4">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Kaggle Featured Competition • $700,000 USD Reward</span>
          </div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight leading-tight">
            ARC Prize 2026 — ARC-AGI-2 Autonomous Solver & Research Pipeline
          </h1>
          <p className="mt-2 text-sm text-slate-300 leading-relaxed">
            A scientifically grounded, neuro-symbolic reasoning system implementing composable
            discrete grid transformations, cellular automata, object-centric reasoning, and strict
            Pass@2 candidate diversity without data contamination.
          </p>
          <div className="mt-5 flex flex-wrap gap-3">
            <button
              onClick={() => onNavigate("playground")}
              className="inline-flex items-center space-x-2 px-4 py-2 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-semibold text-xs shadow-lg shadow-cyan-500/25 transition-all cursor-pointer"
            >
              <Zap className="w-4 h-4" />
              <span>Launch ARC Playground</span>
            </button>
            <button
              onClick={() => onNavigate("submission")}
              className="inline-flex items-center space-x-2 px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-medium text-xs transition-all cursor-pointer"
            >
              <FileCheck className="w-4 h-4" />
              <span>View Verified Submission</span>
            </button>
          </div>
        </div>
        <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-gradient-to-l from-cyan-500/10 to-transparent pointer-events-none" />
      </div>

      {/* Primary KPI Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="glass-card p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium">Best Local Pass@2</span>
            <Trophy className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-cyan-400">
            {(bestExp.val_pass2_acc * 100).toFixed(2)}%
          </div>
          <div className="mt-1 text-[11px] text-slate-400 flex items-center space-x-1">
            <span className="text-emerald-400 font-medium">+1.50%</span>
            <span>over zero baseline</span>
          </div>
        </div>

        <div className="glass-card p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium">Verified Tasks</span>
            <Layers className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-slate-100">
            {qualityReport.summary.total_training_tasks.toLocaleString()}
          </div>
          <div className="mt-1 text-[11px] text-slate-400">
            120 Eval • 240 Test Challenges
          </div>
        </div>

        <div className="glass-card p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium">Submission Schema</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-emerald-400">
            100% PASS
          </div>
          <div className="mt-1 text-[11px] text-slate-400">
            240 tasks • 0 schema errors
          </div>
        </div>

        <div className="glass-card p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium">Inference Latency</span>
            <Clock className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-purple-400">
            {bestExp.avg_latency_ms.toFixed(1)} ms
          </div>
          <div className="mt-1 text-[11px] text-slate-400">
            Per task (CPU lightweight)
          </div>
        </div>
      </div>

      {/* Two Column Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Model Progression */}
        <div className="lg:col-span-2 glass-card p-5 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-sm font-bold text-slate-100 uppercase tracking-wider">
                Ablation Experiment Progression
              </h2>
              <p className="text-xs text-slate-400">
                Controlled incremental benchmarks on validation partition (200 tasks)
              </p>
            </div>
            <button
              onClick={() => onNavigate("experiments")}
              className="text-xs text-cyan-400 hover:text-cyan-300 flex items-center space-x-1"
            >
              <span>Full Tracker</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-900/80 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="py-2.5 px-3 font-semibold">Experiment</th>
                  <th className="py-2.5 px-3 font-semibold">Core Families</th>
                  <th className="py-2.5 px-3 font-semibold text-right">Val Pass@1</th>
                  <th className="py-2.5 px-3 font-semibold text-right">Val Pass@2</th>
                  <th className="py-2.5 px-3 font-semibold text-right">Latency</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono">
                {experimentsData.map((exp: any, idx: number) => (
                  <tr
                    key={exp.experiment_id}
                    className={`hover:bg-slate-800/40 transition-colors ${
                      idx === experimentsData.length - 1 ? "bg-cyan-950/20 text-cyan-300" : ""
                    }`}
                  >
                    <td className="py-2.5 px-3 font-sans font-medium text-slate-200 flex items-center space-x-2">
                      {idx === experimentsData.length - 1 && (
                        <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                      )}
                      <span>{exp.model_version}</span>
                    </td>
                    <td className="py-2.5 px-3 text-slate-400 font-sans truncate max-w-[200px]">
                      {exp.description}
                    </td>
                    <td className="py-2.5 px-3 text-right">
                      {(exp.val_pass1_acc * 100).toFixed(1)}%
                    </td>
                    <td className="py-2.5 px-3 text-right font-bold text-cyan-400">
                      {(exp.val_pass2_acc * 100).toFixed(1)}%
                    </td>
                    <td className="py-2.5 px-3 text-right text-slate-400">
                      {exp.avg_latency_ms.toFixed(1)} ms
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right Column: Competition & Environment Specs */}
        <div className="glass-card p-5 rounded-xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-bold text-slate-100 uppercase tracking-wider">
            Execution Environment
          </h2>
          <div className="space-y-3 text-xs">
            <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
              <span className="text-slate-400">Competition</span>
              <span className="font-medium text-slate-200">ARC Prize 2026 — ARC-AGI-2</span>
            </div>
            <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
              <span className="text-slate-400">Runtime Target</span>
              <span className="font-medium text-slate-200">Kaggle Offline Sandbox</span>
            </div>
            <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
              <span className="text-slate-400">Python Version</span>
              <span className="font-mono text-cyan-400">3.14.6 (Windows x64)</span>
            </div>
            <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
              <span className="text-slate-400">Evaluation Metric</span>
              <span className="font-mono text-cyan-400">Pass@2 Exact Match</span>
            </div>
            <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
              <span className="text-slate-400">Internet Access</span>
              <span className="font-medium text-amber-400">Disabled (Offline Only)</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Git Branch / Remote</span>
              <span className="font-mono text-slate-300">main • arc-agi-2-reasoning-lab</span>
            </div>
          </div>

          <div className="pt-2">
            <div className="p-3 bg-cyan-950/30 rounded-lg border border-cyan-800/40 text-[11px] text-cyan-300">
              <span className="font-semibold">Demonstration Gating Principle:</span> A candidate
              transformation rule is strictly discarded if it fails to explain 100% of the
              demonstration input/output pairs.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
