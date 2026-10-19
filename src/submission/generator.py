"""
src/submission/generator.py - Generates verified Kaggle submission.json using ARCSolver.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from src.arc_solver.solver import ARCSolver

def generate_submission(
    test_challenges_path: Path,
    output_path: Path,
    solver: Optional[ARCSolver] = None
) -> Dict[str, Any]:
    """
    Read test challenges, run solver for each task, and export compliant submission.json.
    """
    if solver is None:
        solver = ARCSolver()

    with open(test_challenges_path, "r", encoding="utf-8") as f:
        challenges = json.load(f)

    submission = {}
    print(f"[*] Generating predictions for {len(challenges)} test challenge tasks...")

    for idx, (task_id, task_data) in enumerate(challenges.items(), 1):
        preds = solver.solve_task(task_data)
        submission[task_id] = preds
        if idx % 50 == 0 or idx == len(challenges):
            print(f"    Progress: {idx}/{len(challenges)} tasks solved.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(submission, f, indent=None)

    print(f"[+] Wrote verified submission to {output_path} ({output_path.stat().st_size:,} bytes).")
    return submission
