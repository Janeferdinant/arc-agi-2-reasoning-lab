#!/usr/bin/env python3
"""
scripts/evaluate.py - Standalone evaluation runner for ARC-AGI-2.

Usage:
    py scripts/evaluate.py --split eval
    py scripts/evaluate.py --split train --max-tasks 50
"""

import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.arc_solver.solver import ARCSolver
from src.evaluation.evaluator import evaluate_dataset_subset

DATA_DIR = BASE_DIR / "data"

def main():
    parser = argparse.ArgumentParser(description="Evaluate ARC-AGI-2 solver.")
    parser.add_argument("--split", choices=["eval", "train"], default="eval", help="Split to evaluate on")
    parser.add_argument("--max-tasks", type=int, default=None, help="Limit number of tasks")
    args = parser.parse_args()

    if args.split == "eval":
        chal_path = DATA_DIR / "arc-agi_evaluation_challenges.json"
        sol_path = DATA_DIR / "arc-agi_evaluation_solutions.json"
    else:
        chal_path = DATA_DIR / "arc-agi_training_challenges.json"
        sol_path = DATA_DIR / "arc-agi_training_solutions.json"

    with open(chal_path, "r", encoding="utf-8") as f:
        challenges = json.load(f)
    with open(sol_path, "r", encoding="utf-8") as f:
        solutions = json.load(f)

    solver = ARCSolver()
    res = evaluate_dataset_subset(challenges, solutions, solver=solver, max_tasks=args.max_tasks)

    print(f"\n--- Evaluation Results ({args.split.upper()} set) ---")
    print(f"Total Tasks Evaluated: {res['total_tasks']}")
    print(f"Tasks Solved Pass@1:   {res['tasks_solved_pass1']} ({res['task_accuracy_pass1']*100:.2f}%)")
    print(f"Tasks Solved Pass@2:   {res['tasks_solved_pass2']} ({res['task_accuracy_pass2']*100:.2f}%)")
    print(f"Total Inputs:          {res['total_inputs']}")
    print(f"Inputs Correct Pass@2: {res['inputs_correct_pass2']} ({res['input_accuracy_pass2']*100:.2f}%)")
    print(f"Total Duration:        {res['total_duration_sec']}s ({res['avg_latency_ms_per_task']}ms / task)")

if __name__ == "__main__":
    main()
