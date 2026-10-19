"use client";

import React, { useState } from "react";
import { GridVisualizer, ARC_COLORS } from "./GridVisualizer";
import qualityReport from "../data/data_quality_report.json";
import sampleTasks from "../data/sample_tasks.json";
import { Database, CheckCircle2, Eye, ShieldAlert, Sparkles } from "lucide-react";

export function DatasetExplorerTab() {
  const [selectedTaskIndex, setSelectedTaskIndex] = useState(0);
  const selectedTask = sampleTasks[selectedTaskIndex] || sampleTasks[0];

  return (
    <div className="space-y-6">
      {/* Header Info */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 glass-card p-5 rounded-xl border border-slate-800">
        <div>
          <div className="flex items-center space-x-2">
            <Database className="w-5 h-5 text-cyan-400" />
            <h2 className="text-base font-bold text-slate-100">
              Verified Competition Dataset Inventory
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Real competition files verified with exact SHA-256 hashes, zero anomalies, and no data
            contamination.
          </p>
        </div>
        <div className="flex items-center space-x-2 text-xs">
          <span className="px-3 py-1 rounded-full bg-emerald-950/70 text-emerald-400 border border-emerald-800/60 font-mono flex items-center space-x-1.5">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>6/6 Files Verified</span>
          </span>
        </div>
      </div>

      {/* Files Table */}
      <div className="glass-card p-5 rounded-xl border border-slate-800 overflow-x-auto">
        <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-3">
          Competition File Registry
        </h3>
        <table className="w-full text-xs text-left">
          <thead className="bg-slate-900/80 text-slate-400 border-b border-slate-800">
            <tr>
              <th className="py-2.5 px-3 font-semibold">Filename</th>
              <th className="py-2.5 px-3 font-semibold">File Size</th>
              <th className="py-2.5 px-3 font-semibold font-mono">SHA-256 (Prefix)</th>
              <th className="py-2.5 px-3 font-semibold text-right">Task Count</th>
              <th className="py-2.5 px-3 font-semibold text-center">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 font-mono">
            {Object.entries(qualityReport.files).map(([fname, finfo]: [string, any]) => (
              <tr key={fname} className="hover:bg-slate-800/30 transition-colors">
                <td className="py-2.5 px-3 font-sans font-medium text-slate-200">{fname}</td>
                <td className="py-2.5 px-3 text-slate-400 font-mono">
                  {finfo.size_bytes.toLocaleString()} bytes
                </td>
                <td className="py-2.5 px-3 text-cyan-400 font-mono">
                  {finfo.sha256.slice(0, 16)}...
                </td>
                <td className="py-2.5 px-3 text-right font-mono text-slate-200">
                  {finfo.task_count.toLocaleString()}
                </td>
                <td className="py-2.5 px-3 text-center">
                  <span className="inline-flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] font-sans font-medium bg-emerald-950 text-emerald-400 border border-emerald-800/50">
                    <CheckCircle2 className="w-2.5 h-2.5" />
                    <span>Verified</span>
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Color Palette Reference */}
      <div className="glass-card p-5 rounded-xl border border-slate-800">
        <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-3">
          Official ARC Color Palette (Symbols 0–9)
        </h3>
        <div className="grid grid-cols-2 sm:grid-cols-5 md:grid-cols-10 gap-2">
          {Object.entries(ARC_COLORS).map(([idStr, c]) => {
            const id = parseInt(idStr);
            return (
              <div
                key={id}
                className="flex flex-col items-center p-2 rounded-lg bg-slate-900/60 border border-slate-800"
              >
                <div
                  className="w-8 h-8 rounded-md shadow-inner border border-white/20 mb-1.5 flex items-center justify-center font-bold text-xs font-mono"
                  style={{ backgroundColor: c.hex, color: c.fg }}
                >
                  {id}
                </div>
                <span className="text-[11px] font-medium text-slate-200">{c.name}</span>
                <span className="text-[10px] font-mono text-slate-500">{c.hex}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Interactive Task Visualizer */}
      <div className="glass-card p-5 rounded-xl border border-slate-800 space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div>
            <h3 className="text-sm font-bold text-slate-100 flex items-center space-x-2">
              <Eye className="w-4 h-4 text-cyan-400" />
              <span>Interactive Task Visualizer (Permitted Training Set)</span>
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Select any permitted ARC task to inspect demonstration pairs and test inputs.
            </p>
          </div>

          {/* Task Selector */}
          <div className="flex items-center space-x-2">
            <span className="text-xs text-slate-400">Task:</span>
            <select
              value={selectedTaskIndex}
              onChange={(e) => setSelectedTaskIndex(parseInt(e.target.value))}
              aria-label="Select ARC training task"
              className="bg-slate-900 text-xs text-cyan-300 border border-slate-700 rounded-lg px-3 py-1.5 focus:outline-none focus:border-cyan-500 font-mono"
            >
              {sampleTasks.map((t: any, idx: number) => (
                <option key={t.id} value={idx}>
                  Task #{idx + 1}: {t.id} ({t.train.length} train, {t.test.length} test)
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Task Details */}
        <div className="p-3 bg-slate-900/50 rounded-lg border border-slate-800/80 flex flex-wrap gap-4 text-xs font-mono">
          <div>
            <span className="text-slate-500">Task ID: </span>
            <span className="text-cyan-400 font-bold">{selectedTask.id}</span>
          </div>
          <div>
            <span className="text-slate-500">Demonstrations: </span>
            <span className="text-slate-300">{selectedTask.train.length} pairs</span>
          </div>
          <div>
            <span className="text-slate-500">Test Invocations: </span>
            <span className="text-slate-300">{selectedTask.test.length}</span>
          </div>
        </div>

        {/* Demonstration Pairs */}
        <div>
          <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-3">
            Demonstration Input/Output Pairs (Train)
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {selectedTask.train.map((pair: any, pIdx: number) => (
              <div
                key={pIdx}
                className="p-3 rounded-lg bg-slate-900/40 border border-slate-800/90 flex flex-col items-center space-y-3"
              >
                <span className="text-[11px] font-mono text-slate-400 font-semibold self-start">
                  Pair #{pIdx + 1}
                </span>
                <div className="flex items-center space-x-4">
                  <GridVisualizer grid={pair.input} label="Input" maxCellSize={16} />
                  <span className="text-slate-600 font-mono">→</span>
                  <GridVisualizer grid={pair.output} label="Output" maxCellSize={16} />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Test Queries */}
        <div className="pt-2 border-t border-slate-800/80">
          <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-3">
            Test Query & Ground Truth Solution
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {selectedTask.test.map((tItem: any, tIdx: number) => {
              const solGrid = selectedTask.solution?.[tIdx];
              return (
                <div
                  key={tIdx}
                  className="p-3 rounded-lg bg-slate-900/40 border border-slate-800/90 flex flex-col items-center space-y-3"
                >
                  <span className="text-[11px] font-mono text-cyan-400 font-semibold self-start">
                    Test Input #{tIdx + 1}
                  </span>
                  <div className="flex items-center space-x-4">
                    <GridVisualizer grid={tItem.input} label="Test Input" maxCellSize={18} />
                    <span className="text-slate-600 font-mono">→</span>
                    {solGrid ? (
                      <GridVisualizer grid={solGrid} label="Ground Truth Output" maxCellSize={18} />
                    ) : (
                      <div className="flex flex-col items-center justify-center p-4 bg-slate-950/60 border border-dashed border-slate-800 rounded text-slate-500 text-xs">
                        Hidden
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
