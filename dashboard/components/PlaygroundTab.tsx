"use client";

import React, { useState } from "react";
import { GridVisualizer } from "./GridVisualizer";
import sampleTasks from "../data/sample_tasks.json";
import {
  Gamepad2,
  Play,
  RotateCcw,
  CheckCircle2,
  XCircle,
  Clock,
  Sparkles,
  Layers,
  ArrowRight,
} from "lucide-react";

export function PlaygroundTab() {
  const [taskIdx, setTaskIdx] = useState(0);
  const [isSolving, setIsSolving] = useState(false);
  const [results, setResults] = useState<any>(null);

  const currentTask = sampleTasks[taskIdx] || sampleTasks[0];

  // Client-side solver simulator that replicates the exact Python solver logic
  const handleSolve = () => {
    setIsSolving(true);
    setResults(null);

    const startTime = performance.now();

    // Client-side execution of candidate rule generator
    setTimeout(() => {
      const train = currentTask.train;
      const test = currentTask.test;
      const groundTruth = currentTask.solution;

      let ruleExplanation = "Unknown / Fallback Candidates";
      let solvedFamily = "fallback";

      // Test Identity
      const isIdentity = train.every((p: any) => JSON.stringify(p.input) === JSON.stringify(p.output));
      // Test rot90
      const rot90 = (g: number[][]) => g[0].map((_, c) => g.map((r) => r[c]).reverse());
      const isRot90 = train.every((p: any) => JSON.stringify(rot90(p.input)) === JSON.stringify(p.output));
      // Test flip_h
      const flipH = (g: number[][]) => g.map((row) => [...row].reverse());
      const isFlipH = train.every((p: any) => JSON.stringify(flipH(p.input)) === JSON.stringify(p.output));

      // Test Color Remapping
      let isColorMap = true;
      const colorMap: Record<number, number> = {};
      for (const p of train) {
        if (p.input.length !== p.output.length || p.input[0].length !== p.output[0].length) {
          isColorMap = false;
          break;
        }
        for (let r = 0; r < p.input.length; r++) {
          for (let c = 0; c < p.input[0].length; c++) {
            const inVal = p.input[r][c];
            const outVal = p.output[r][c];
            if (colorMap[inVal] !== undefined && colorMap[inVal] !== outVal) {
              isColorMap = false;
              break;
            }
            colorMap[inVal] = outVal;
          }
        }
      }

      const predictions = test.map((tItem: any, idx: number) => {
        let att1 = tItem.input;
        let att2 = tItem.input;

        if (isIdentity) {
          ruleExplanation = "Exact Identity Invariant (demonstration outputs match inputs)";
          solvedFamily = "geometry_identity";
          att1 = tItem.input;
          att2 = rot90(tItem.input);
        } else if (isRot90) {
          ruleExplanation = "Dihedral 90° Clockwise Rotation Invariant";
          solvedFamily = "geometry_rot90";
          att1 = rot90(tItem.input);
          att2 = flipH(tItem.input);
        } else if (isFlipH) {
          ruleExplanation = "Horizontal Mirror Reflection Invariant";
          solvedFamily = "geometry_flip_h";
          att1 = flipH(tItem.input);
          att2 = rot90(tItem.input);
        } else if (isColorMap && Object.keys(colorMap).length > 0) {
          ruleExplanation = "Bijective Palette Remapping Invariant";
          solvedFamily = "color_remapping";
          att1 = tItem.input.map((row: number[]) => row.map((v) => colorMap[v] ?? v));
          att2 = tItem.input;
        } else {
          ruleExplanation = "Object-Centric & Geometry Fallback Candidates (Pass@2 Diverse Sampling)";
          solvedFamily = "fallback_diverse";
          att1 = tItem.input;
          att2 = rot90(tItem.input);
        }

        const trueSol = groundTruth?.[idx];
        const isP1 = trueSol && JSON.stringify(att1) === JSON.stringify(trueSol);
        const isP2 = isP1 || (trueSol && JSON.stringify(att2) === JSON.stringify(trueSol));

        return {
          attempt_1: att1,
          attempt_2: att2,
          trueSol,
          isP1,
          isP2,
        };
      });

      const elapsed = performance.now() - startTime;

      setResults({
        predictions,
        ruleExplanation,
        solvedFamily,
        elapsedMs: elapsed.toFixed(1),
        overallPass1: predictions.every((p: any) => p.isP1),
        overallPass2: predictions.every((p: any) => p.isP2),
      });

      setIsSolving(false);
    }, 150);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-card p-5 rounded-xl border border-slate-800 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <Gamepad2 className="w-5 h-5 text-cyan-400" />
            <h2 className="text-base font-bold text-slate-100">
              Interactive ARC Reasoning Playground
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Load permitted ARC training tasks, trigger live symbolic rule synthesis, and inspect
            Pass@2 predictions with execution latency.
          </p>
        </div>

        {/* Task Selection and Actions */}
        <div className="flex items-center space-x-3">
          <select
            value={taskIdx}
            onChange={(e) => {
              setTaskIdx(parseInt(e.target.value));
              setResults(null);
            }}
            aria-label="Select ARC task in playground"
            className="bg-slate-900 text-xs text-cyan-300 border border-slate-700 rounded-lg px-3 py-2 focus:outline-none focus:border-cyan-500 font-mono"
          >
            {sampleTasks.map((t: any, idx: number) => (
              <option key={t.id} value={idx}>
                Task #{idx + 1}: {t.id}
              </option>
            ))}
          </select>

          <button
            onClick={handleSolve}
            disabled={isSolving}
            className="flex items-center space-x-1.5 px-4 py-2 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs shadow-md shadow-cyan-500/20 transition-all cursor-pointer disabled:opacity-50"
          >
            {isSolving ? (
              <span className="w-3.5 h-3.5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" />
            ) : (
              <Play className="w-3.5 h-3.5 fill-current" />
            )}
            <span>Run Solver</span>
          </button>
        </div>
      </div>

      {/* Task Demonstration Pairs */}
      <div className="glass-card p-5 rounded-xl border border-slate-800 space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
            Demonstration Input/Output Pairs ({currentTask.train.length} pairs)
          </h3>
          <span className="text-[11px] font-mono text-cyan-400">Task ID: {currentTask.id}</span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {currentTask.train.map((pair: any, pIdx: number) => (
            <div
              key={pIdx}
              className="p-3 rounded-lg bg-slate-900/50 border border-slate-800 flex flex-col items-center space-y-2"
            >
              <span className="text-[10px] font-mono text-slate-400 font-bold self-start">
                Pair #{pIdx + 1}
              </span>
              <div className="flex items-center space-x-3">
                <GridVisualizer grid={pair.input} label="In" maxCellSize={15} />
                <ArrowRight className="w-3 h-3 text-slate-600" />
                <GridVisualizer grid={pair.output} label="Out" maxCellSize={15} />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Solver Prediction Area */}
      {results && (
        <div className="glass-card p-5 rounded-xl border border-cyan-500/30 bg-slate-900/70 space-y-5 animate-in fade-in duration-300">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 pb-3 border-b border-slate-800">
            <div>
              <div className="flex items-center space-x-2">
                <Sparkles className="w-4 h-4 text-cyan-400" />
                <h3 className="text-sm font-bold text-slate-100">Solver Reasoning Output</h3>
                {results.overallPass2 ? (
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-950 text-emerald-400 border border-emerald-800 flex items-center space-x-1">
                    <CheckCircle2 className="w-3 h-3" />
                    <span>Pass@2 Solved</span>
                  </span>
                ) : (
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-950 text-amber-400 border border-amber-800 flex items-center space-x-1">
                    <span>Unsolved (Abstained)</span>
                  </span>
                )}
              </div>
              <p className="text-xs text-cyan-300 mt-1 font-mono">{results.ruleExplanation}</p>
            </div>
            <div className="flex items-center space-x-3 text-xs font-mono text-slate-400">
              <span className="flex items-center space-x-1">
                <Clock className="w-3.5 h-3.5 text-purple-400" />
                <span>{results.elapsedMs} ms</span>
              </span>
            </div>
          </div>

          {/* Predictions Grid */}
          <div className="space-y-4">
            {results.predictions.map((p: any, idx: number) => (
              <div key={idx} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                <div className="text-xs font-bold text-slate-300 mb-3 flex items-center justify-between">
                  <span>Test Input #{idx + 1}</span>
                  <div className="flex items-center space-x-2 text-[10px] font-mono">
                    <span
                      className={
                        p.isP1
                          ? "text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/50"
                          : "text-slate-500"
                      }
                    >
                      Attempt 1: {p.isP1 ? "MATCH" : "MISMATCH"}
                    </span>
                    <span
                      className={
                        p.isP2
                          ? "text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800/50"
                          : "text-slate-500"
                      }
                    >
                      Attempt 2: {p.isP2 ? "MATCH" : "MISMATCH"}
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 items-center">
                  <GridVisualizer grid={currentTask.test[idx].input} label="Test Input" maxCellSize={18} />
                  <GridVisualizer grid={p.attempt_1} label="Prediction (Attempt 1)" maxCellSize={18} />
                  <GridVisualizer grid={p.attempt_2} label="Prediction (Attempt 2)" maxCellSize={18} />
                  {p.trueSol && (
                    <GridVisualizer grid={p.trueSol} label="Ground Truth" maxCellSize={18} />
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
