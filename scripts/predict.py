#!/usr/bin/env python3
"""
scripts/predict.py - Inference runner for a single task JSON or challenges dictionary.
"""

import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.arc_solver.solver import ARCSolver

def main():
    parser = argparse.ArgumentParser(description="Predict solutions for an ARC task.")
    parser.add_argument("--task-file", type=str, required=True, help="Path to task JSON file")
    args = parser.parse_args()

    task_path = Path(args.task_file)
    if not task_path.exists():
        print(f"[-] Task file {task_path} does not exist.")
        sys.exit(1)

    with open(task_path, "r", encoding="utf-8") as f:
        task_data = json.load(f)

    solver = ARCSolver()
    predictions = solver.solve_task(task_data)

    print(json.dumps(predictions, indent=2))

if __name__ == "__main__":
    main()
