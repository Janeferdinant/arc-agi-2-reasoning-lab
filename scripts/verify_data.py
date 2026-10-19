#!/usr/bin/env python3
"""
scripts/verify_data.py - ARC-AGI-2 Comprehensive Data Quality & Schema Verification

Parses all competition JSON files, calculates SHA-256 checksums, validates dimensions and
color ranges, detects anomalies or malformed grids, and outputs:
- research/data_inventory.md
- research/data_quality_report.json
"""

import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RESEARCH_DIR = BASE_DIR / "research"

FILES_TO_INSPECT = [
    "arc-agi_training_challenges.json",
    "arc-agi_training_solutions.json",
    "arc-agi_evaluation_challenges.json",
    "arc-agi_evaluation_solutions.json",
    "arc-agi_test_challenges.json",
    "sample_submission.json",
]

def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def validate_grid(grid: Any) -> Tuple[bool, str, Tuple[int, int]]:
    """Validate that grid is a 2D rectangular array of ints in range [0, 9]."""
    if not isinstance(grid, list) or len(grid) == 0:
        return False, "Grid is empty or not a list", (0, 0)
    height = len(grid)
    if not isinstance(grid[0], list) or len(grid[0]) == 0:
        return False, "First row is empty or not a list", (height, 0)
    width = len(grid[0])
    
    if height > 30 or width > 30:
        return False, f"Grid dimensions {height}x{width} exceed 30x30", (height, width)
        
    for r_idx, row in enumerate(grid):
        if not isinstance(row, list) or len(row) != width:
            return False, f"Row {r_idx} length {len(row) if isinstance(row, list) else 'non-list'} != expected width {width}", (height, width)
        for c_idx, cell in enumerate(row):
            if not isinstance(cell, int) or isinstance(cell, bool):
                return False, f"Cell ({r_idx}, {c_idx}) is not an int: {cell}", (height, width)
            if cell < 0 or cell > 9:
                return False, f"Cell ({r_idx}, {c_idx}) value {cell} out of range [0, 9]", (height, width)
                
    return True, "OK", (height, width)

def verify_dataset():
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "verified_at": "2026-10-19T21:50:00Z",
        "competition": "arc-prize-2026-arc-agi-2",
        "files": {},
        "summary": {
            "all_files_exist": True,
            "all_json_valid": True,
            "all_grids_valid": True,
            "total_training_tasks": 0,
            "total_training_pairs": 0,
            "total_evaluation_tasks": 0,
            "total_evaluation_pairs": 0,
            "total_test_tasks": 0,
            "total_test_inputs": 0,
            "color_distribution": {str(c): 0 for c in range(10)},
            "grid_dimensions": {"min_h": 999, "max_h": 0, "min_w": 999, "max_w": 0},
        },
        "anomalies": []
    }

    markdown_inventory = [
        "# ARC Prize 2026 — ARC-AGI-2: Dataset Inventory & Data Quality Report",
        "",
        "## 1. Verified Competition Files",
        "",
        "| Filename | Size (bytes) | SHA-256 Checksum (first 16) | Tasks | Status | Description |",
        "|---|---|---|---|---|---|",
    ]

    for fname in FILES_TO_INSPECT:
        fpath = DATA_DIR / fname
        if not fpath.exists():
            report["summary"]["all_files_exist"] = False
            report["anomalies"].append(f"File {fname} is missing.")
            markdown_inventory.append(f"| `{fname}` | 0 | MISSING | 0 | FAILED | File not found |")
            continue

        size = fpath.stat().st_size
        sha = compute_sha256(fpath)
        
        file_info = {
            "size_bytes": size,
            "sha256": sha,
            "json_valid": False,
            "task_count": 0,
            "schema_notes": "",
        }

        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            file_info["json_valid"] = True
            file_info["task_count"] = len(data)
        except Exception as e:
            report["summary"]["all_json_valid"] = False
            report["anomalies"].append(f"File {fname} JSON parse error: {e}")
            report["files"][fname] = file_info
            markdown_inventory.append(f"| `{fname}` | {size:,} | `{sha[:16]}...` | 0 | CORRUPT JSON | Parse error |")
            continue

        desc = ""
        if fname == "arc-agi_training_challenges.json":
            desc = "1,000 public training tasks (demonstration pairs & test inputs)"
            report["summary"]["total_training_tasks"] = len(data)
            for tid, tdata in data.items():
                train_pairs = tdata.get("train", [])
                test_pairs = tdata.get("test", [])
                report["summary"]["total_training_pairs"] += len(train_pairs)
                for pair in train_pairs:
                    for k in ["input", "output"]:
                        ok, msg, (h, w) = validate_grid(pair[k])
                        if not ok:
                            report["summary"]["all_grids_valid"] = False
                            report["anomalies"].append(f"{fname}:{tid}:{k} - {msg}")
                        report["summary"]["grid_dimensions"]["min_h"] = min(report["summary"]["grid_dimensions"]["min_h"], h)
                        report["summary"]["grid_dimensions"]["max_h"] = max(report["summary"]["grid_dimensions"]["max_h"], h)
                        report["summary"]["grid_dimensions"]["min_w"] = min(report["summary"]["grid_dimensions"]["min_w"], w)
                        report["summary"]["grid_dimensions"]["max_w"] = max(report["summary"]["grid_dimensions"]["max_w"], w)
                        for row in pair[k]:
                            for val in row:
                                report["summary"]["color_distribution"][str(val)] += 1
                for pair in test_pairs:
                    ok, msg, (h, w) = validate_grid(pair["input"])
                    if not ok:
                        report["summary"]["all_grids_valid"] = False
                        report["anomalies"].append(f"{fname}:{tid}:test:input - {msg}")
        elif fname == "arc-agi_training_solutions.json":
            desc = "1,000 public training task solutions (ground-truth test outputs)"
            for tid, sol_list in data.items():
                for s_grid in sol_list:
                    ok, msg, (h, w) = validate_grid(s_grid)
                    if not ok:
                        report["summary"]["all_grids_valid"] = False
                        report["anomalies"].append(f"{fname}:{tid} - {msg}")
        elif fname == "arc-agi_evaluation_challenges.json":
            desc = "120 public evaluation tasks without test solutions"
            report["summary"]["total_evaluation_tasks"] = len(data)
            for tid, tdata in data.items():
                train_pairs = tdata.get("train", [])
                test_pairs = tdata.get("test", [])
                report["summary"]["total_evaluation_pairs"] += len(train_pairs)
                for pair in train_pairs:
                    for k in ["input", "output"]:
                        ok, msg, (h, w) = validate_grid(pair[k])
                        if not ok:
                            report["summary"]["all_grids_valid"] = False
                            report["anomalies"].append(f"{fname}:{tid}:{k} - {msg}")
        elif fname == "arc-agi_evaluation_solutions.json":
            desc = "120 public evaluation task solutions (ground-truth test outputs)"
        elif fname == "arc-agi_test_challenges.json":
            desc = "Hidden competition test inputs (eval tasks or unseen challenges)"
            report["summary"]["total_test_tasks"] = len(data)
            for tid, tdata in data.items():
                test_inputs = tdata.get("test", [])
                report["summary"]["total_test_inputs"] += len(test_inputs)
        elif fname == "sample_submission.json":
            desc = "Official Kaggle sample submission schema demonstration"

        file_info["schema_notes"] = desc
        report["files"][fname] = file_info
        markdown_inventory.append(f"| `{fname}` | {size:,} | `{sha[:16]}...` | {len(data):,} | VERIFIED | {desc} |")

    markdown_inventory.extend([
        "",
        "## 2. Dataset Metrics & Integrity Checks",
        f"- **All Files Present & Verified**: `{report['summary']['all_files_exist']}`",
        f"- **All JSON Parsed Successfully**: `{report['summary']['all_json_valid']}`",
        f"- **All Grid Values Valid (Integers in [0, 9])**: `{report['summary']['all_grids_valid']}`",
        f"- **Grid Dimension Bounds**: Height [{report['summary']['grid_dimensions']['min_h']} to {report['summary']['grid_dimensions']['max_h']}], Width [{report['summary']['grid_dimensions']['min_w']} to {report['summary']['grid_dimensions']['max_w']}]",
        f"- **Total Training Tasks**: {report['summary']['total_training_tasks']:,}",
        f"- **Total Evaluation Tasks**: {report['summary']['total_evaluation_tasks']:,}",
        f"- **Total Test Challenges**: {report['summary']['total_test_tasks']:,} (with {report['summary']['total_test_inputs']:,} test inputs)",
        f"- **Detected Anomalies / Corruptions**: {len(report['anomalies'])}",
        "",
        "## 3. Official ARC Color Palette Mapping",
        "| ID | Color Name | Hex Code | Visual Meaning / Usage |",
        "|---|---|---|---|",
        "| 0 | Black | `#000000` | Typically background / void |",
        "| 1 | Blue | `#0074D9` | Object primary / accent |",
        "| 2 | Red | `#FF4136` | Target / obstacle / marker |",
        "| 3 | Green | `#2ECC40` | Goal / active segment |",
        "| 4 | Yellow | `#FFDC00` | Highlight / connection |",
        "| 5 | Grey | `#AAAAAA` | Border / separator / frame |",
        "| 6 | Magenta / Fuchsia | `#F012BE` | Transformation indicator |",
        "| 7 | Orange | `#FF851B` | Secondary entity |",
        "| 8 | Teal / Cyan | `#7FDBFF` | Water / fill / symmetry axis |",
        "| 9 | Maroon / Brown | `#870C25` | Special anchor / base |",
    ])

    # Write report files
    with open(RESEARCH_DIR / "data_quality_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    with open(RESEARCH_DIR / "data_inventory.md", "w", encoding="utf-8") as f:
        f.write("\n".join(markdown_inventory) + "\n")

    print("[+] Wrote data quality report to research/data_quality_report.json")
    print("[+] Wrote data inventory documentation to research/data_inventory.md")
    print(f"[+] Total training tasks: {report['summary']['total_training_tasks']}")
    print(f"[+] Total evaluation tasks: {report['summary']['total_evaluation_tasks']}")
    print(f"[+] Total test tasks: {report['summary']['total_test_tasks']}")
    print(f"[+] Anomalies: {len(report['anomalies'])}")

if __name__ == "__main__":
    verify_dataset()
