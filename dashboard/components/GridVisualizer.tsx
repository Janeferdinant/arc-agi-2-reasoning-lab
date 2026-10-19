"use client";

import React from "react";

export const ARC_COLORS: Record<number, { name: string; hex: string; fg: string }> = {
  0: { name: "Black", hex: "#000000", fg: "#ffffff" },
  1: { name: "Blue", hex: "#0074D9", fg: "#ffffff" },
  2: { name: "Red", hex: "#FF4136", fg: "#ffffff" },
  3: { name: "Green", hex: "#2ECC40", fg: "#000000" },
  4: { name: "Yellow", hex: "#FFDC00", fg: "#000000" },
  5: { name: "Grey", hex: "#AAAAAA", fg: "#000000" },
  6: { name: "Magenta", hex: "#F012BE", fg: "#ffffff" },
  7: { name: "Orange", hex: "#FF851B", fg: "#000000" },
  8: { name: "Teal", hex: "#7FDBFF", fg: "#000000" },
  9: { name: "Maroon", hex: "#870C25", fg: "#ffffff" },
};

interface GridVisualizerProps {
  grid: number[][];
  label?: string;
  maxCellSize?: number;
  showCoordinates?: boolean;
}

export function GridVisualizer({
  grid,
  label,
  maxCellSize = 24,
  showCoordinates = false,
}: GridVisualizerProps) {
  if (!grid || !grid.length || !grid[0].length) {
    return (
      <div className="flex flex-col items-center justify-center p-4 bg-slate-900/50 rounded-lg border border-slate-800 text-slate-500 text-xs">
        Empty Grid
      </div>
    );
  }

  const height = grid.length;
  const width = grid[0].length;

  return (
    <div className="flex flex-col items-center">
      {label && (
        <div className="flex items-center justify-between w-full mb-1.5 px-1">
          <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
            {label}
          </span>
          <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950/60 px-1.5 py-0.5 rounded border border-cyan-800/50">
            {height}×{width}
          </span>
        </div>
      )}
      <div
        className="grid gap-[1px] bg-slate-800/80 p-1 rounded border border-slate-700/80 shadow-md inline-block"
        style={{
          gridTemplateColumns: `repeat(${width}, minmax(0, 1fr))`,
        }}
      >
        {grid.map((row, rIdx) =>
          row.map((cell, cIdx) => {
            const colorMeta = ARC_COLORS[cell] || { hex: "#333333", fg: "#fff" };
            return (
              <div
                key={`${rIdx}-${cIdx}`}
                className="arc-grid-cell rounded-[1px] flex items-center justify-center font-mono cursor-pointer relative group"
                style={{
                  backgroundColor: colorMeta.hex,
                  width: `${Math.min(maxCellSize, 280 / Math.max(width, height))}px`,
                  height: `${Math.min(maxCellSize, 280 / Math.max(width, height))}px`,
                }}
                title={`(${rIdx}, ${cIdx}) Color ${cell} (${colorMeta.name})`}
              >
                {showCoordinates && (
                  <span
                    className="text-[8px] font-bold opacity-0 group-hover:opacity-100 transition-opacity"
                    style={{ color: colorMeta.fg }}
                  >
                    {cell}
                  </span>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
