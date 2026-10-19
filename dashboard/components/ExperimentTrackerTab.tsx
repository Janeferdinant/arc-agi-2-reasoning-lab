"use client";

import React, { useState } from "react";
import experimentsData from "../data/experiments.json";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { BarChart3, Filter, ArrowUpDown, Download, CheckCircle2 } from "lucide-react";

export function ExperimentTrackerTab() {
  const [sortBy, setSortBy] = useState<"id" | "score" | "latency">("id");
  const [filterQuery, setFilterQuery] = useState("");

  const chartData = experimentsData.map((e: any) => ({
    name: e.model_version.replace("solver_", "").replace("baseline_", "b_"),
    fullName: e.model_version,
    "Val Pass@1 (%)": parseFloat((e.val_pass1_acc * 100).toFixed(2)),
    "Val Pass@2 (%)": parseFloat((e.val_pass2_acc * 100).toFixed(2)),
    "Latency (ms)": parseFloat(e.avg_latency_ms.toFixed(1)),
  }));

  const filtered = experimentsData.filter(
    (e: any) =>
      e.model_version.toLowerCase().includes(filterQuery.toLowerCase()) ||
      e.description.toLowerCase().includes(filterQuery.toLowerCase())
  );

  const sorted = [...filtered].sort((a: any, b: any) => {
    if (sortBy === "score") return b.val_pass2_acc - a.val_pass2_acc;
    if (sortBy === "latency") return a.avg_latency_ms - b.avg_latency_ms;
    return a.experiment_id.localeCompare(b.experiment_id);
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-card p-5 rounded-xl border border-slate-800 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <BarChart3 className="w-5 h-5 text-cyan-400" />
            <h2 className="text-base font-bold text-slate-100">
              Systematic Experiment Tracker & Ablation Studies
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Empirical comparisons across baseline symbolic invariants, discrete color mappings, and
            Pass@2 diversity ranking.
          </p>
        </div>
      </div>

      {/* Chart Section */}
      <div className="glass-card p-5 rounded-xl border border-slate-800 space-y-4">
        <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
          Validation Accuracy by Solver Architecture (Pass@1 vs Pass@2)
        </h3>
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 25 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="name" stroke="#64748b" tick={{ fontSize: 11 }} />
              <YAxis stroke="#64748b" tick={{ fontSize: 11 }} unit="%" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#0f172a",
                  borderColor: "#334155",
                  borderRadius: "8px",
                  fontSize: "12px",
                }}
              />
              <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "8px" }} />
              <Bar dataKey="Val Pass@1 (%)" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Val Pass@2 (%)" fill="#06b6d4" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Table Section with Filter & Sort */}
      <div className="glass-card p-5 rounded-xl border border-slate-800 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div className="flex items-center space-x-2 flex-1 max-w-sm">
            <Filter className="w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Filter by name or description..."
              value={filterQuery}
              onChange={(e) => setFilterQuery(e.target.value)}
              className="bg-slate-900 text-xs text-slate-200 border border-slate-700 rounded-lg px-3 py-1.5 w-full focus:outline-none focus:border-cyan-500"
            />
          </div>

          <div className="flex items-center space-x-2">
            <span className="text-xs text-slate-400">Sort by:</span>
            <select
              value={sortBy}
              onChange={(e: any) => setSortBy(e.target.value)}
              aria-label="Sort experiments by"
              className="bg-slate-900 text-xs text-cyan-300 border border-slate-700 rounded-lg px-3 py-1.5 focus:outline-none focus:border-cyan-500 font-mono"
            >
              <option value="id">ID (Default)</option>
              <option value="score">Pass@2 Score (High to Low)</option>
              <option value="latency">Latency (Fastest First)</option>
            </select>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-900/80 text-slate-400 border-b border-slate-800">
              <tr>
                <th className="py-2.5 px-3 font-semibold">ID</th>
                <th className="py-2.5 px-3 font-semibold">Model Version</th>
                <th className="py-2.5 px-3 font-semibold">Architecture Description</th>
                <th className="py-2.5 px-3 font-semibold text-right">Val Pass@1</th>
                <th className="py-2.5 px-3 font-semibold text-right">Val Pass@2</th>
                <th className="py-2.5 px-3 font-semibold text-right">Eval Pass@2</th>
                <th className="py-2.5 px-3 font-semibold text-right">Latency / Task</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono">
              {sorted.map((exp: any) => (
                <tr key={exp.experiment_id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="py-2.5 px-3 text-cyan-400 font-bold">{exp.experiment_id}</td>
                  <td className="py-2.5 px-3 font-sans font-medium text-slate-200">
                    {exp.model_version}
                  </td>
                  <td className="py-2.5 px-3 text-slate-400 font-sans">{exp.description}</td>
                  <td className="py-2.5 px-3 text-right">
                    {(exp.val_pass1_acc * 100).toFixed(2)}%
                  </td>
                  <td className="py-2.5 px-3 text-right text-cyan-400 font-bold">
                    {(exp.val_pass2_acc * 100).toFixed(2)}%
                  </td>
                  <td className="py-2.5 px-3 text-right text-slate-300">
                    {(exp.eval_pass2_acc * 100).toFixed(2)}%
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
    </div>
  );
}
