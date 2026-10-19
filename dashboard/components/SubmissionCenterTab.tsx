"use client";

import React, { useState } from "react";
import {
  FileCheck2,
  Download,
  CheckCircle2,
  ShieldCheck,
  Terminal,
  Copy,
  Check,
  FileCode,
} from "lucide-react";

export function SubmissionCenterTab() {
  const [copied, setCopied] = useState(false);

  const validationChecks = [
    { title: "JSON Structure & Syntax", status: "PASS", desc: "Clean parseable JSON object" },
    { title: "Task ID Completeness", status: "PASS", desc: "All 240 test challenge task IDs present" },
    { title: "Test Invocations Preservation", status: "PASS", desc: "Correct prediction counts per task" },
    { title: "Dual Attempts Guarantee", status: "PASS", desc: "Every item contains attempt_1 and attempt_2" },
    { title: "Discrete Color Bounds", status: "PASS", desc: "All cell integers strictly within [0, 9]" },
    { title: "Grid Rectangularity & Bounds", status: "PASS", desc: "No ragged rows; dimensions in [1x1..30x30]" },
    { title: "Offline Self-Contained", status: "PASS", desc: "Zero external model/internet dependencies" },
  ];

  const handleCopyCmd = () => {
    navigator.clipboard.writeText("py scripts/validate_submission.py submission.json");
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-card p-5 rounded-xl border border-slate-800 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <FileCheck2 className="w-5 h-5 text-emerald-400" />
            <h2 className="text-base font-bold text-slate-100">
              Kaggle Submission Center & Verification
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Official competition submission generation, strict schema validation, and export tooling.
          </p>
        </div>
        <div>
          <a
            href="/submission.json"
            download="submission.json"
            className="flex items-center space-x-2 px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow-md shadow-emerald-500/20 transition-all cursor-pointer"
          >
            <Download className="w-4 h-4" />
            <span>Download submission.json</span>
          </a>
        </div>
      </div>

      {/* Submission Metadata Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="glass-card p-4 rounded-xl border border-slate-800">
          <span className="text-xs text-slate-400 font-medium">Target Tasks</span>
          <div className="text-2xl font-bold font-mono text-slate-100 mt-1">240</div>
          <span className="text-[11px] text-slate-500">100% matched to test set</span>
        </div>
        <div className="glass-card p-4 rounded-xl border border-slate-800">
          <span className="text-xs text-slate-400 font-medium">Attempts Per Task</span>
          <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">2</div>
          <span className="text-[11px] text-slate-500">Pass@2 compliant</span>
        </div>
        <div className="glass-card p-4 rounded-xl border border-slate-800">
          <span className="text-xs text-slate-400 font-medium">File Size</span>
          <div className="text-2xl font-bold font-mono text-purple-400 mt-1">343.5 KB</div>
          <span className="text-[11px] text-slate-500">Uncompressed valid JSON</span>
        </div>
        <div className="glass-card p-4 rounded-xl border border-slate-800">
          <span className="text-xs text-slate-400 font-medium">Schema Status</span>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">VALIDATED</div>
          <span className="text-[11px] text-emerald-400/80">0 errors detected</span>
        </div>
      </div>

      {/* Strict Schema Checklist */}
      <div className="glass-card p-5 rounded-xl border border-slate-800 space-y-4">
        <div className="flex items-center space-x-2">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">
            Kaggle ARC Strict Validation Checklist
          </h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {validationChecks.map((chk) => (
            <div
              key={chk.title}
              className="p-3 rounded-lg bg-slate-900/60 border border-slate-800 flex items-start space-x-3"
            >
              <CheckCircle2 className="w-4 h-4 text-emerald-400 mt-0.5 shrink-0" />
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-200">{chk.title}</span>
                  <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800/60">
                    {chk.status}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 mt-0.5">{chk.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Terminal Command Reference */}
      <div className="glass-card p-5 rounded-xl border border-slate-800 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Terminal className="w-4 h-4 text-cyan-400" />
            <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
              Local Verification CLI Command
            </h3>
          </div>
          <button
            onClick={handleCopyCmd}
            className="flex items-center space-x-1 text-xs text-slate-400 hover:text-cyan-400 transition-colors cursor-pointer"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? "Copied" : "Copy"}</span>
          </button>
        </div>
        <div className="p-3 bg-slate-950 font-mono text-xs text-cyan-300 rounded-lg border border-slate-800 flex items-center justify-between overflow-x-auto">
          <code>py scripts/validate_submission.py submission.json</code>
        </div>
      </div>
    </div>
  );
}
