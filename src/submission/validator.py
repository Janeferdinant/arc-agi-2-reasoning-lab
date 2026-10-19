"""
src/submission/validator.py - Strict Kaggle ARC submission schema validator.
"""

from typing import Any, Dict, List, Optional, Tuple

def validate_submission_dict(
    submission: Any,
    expected_tasks: Dict[str, int]
) -> Tuple[bool, List[str]]:
    """
    Validate submission JSON data against Kaggle competition requirements:
    1. Must be a JSON dictionary mapping task_id -> list of predictions.
    2. Must contain every expected task_id.
    3. Prediction list length must match expected test input count.
    4. Each prediction dict must contain exactly 'attempt_1' and 'attempt_2'.
    5. Each attempt must be a valid 2D rectangular grid of integers in [0, 9].
    6. Grid dimensions must be between 1x1 and 30x30.
    """
    errors: List[str] = []

    if not isinstance(submission, dict):
        return False, ["Submission must be a top-level JSON dictionary."]

    # Check for missing tasks
    missing_tasks = set(expected_tasks.keys()) - set(submission.keys())
    if missing_tasks:
        for tid in sorted(missing_tasks):
            errors.append(f"Missing task ID: {tid}")

    # Check for unexpected tasks
    unexpected_tasks = set(submission.keys()) - set(expected_tasks.keys())
    if unexpected_tasks:
        for tid in sorted(unexpected_tasks):
            errors.append(f"Unexpected task ID: {tid}")

    # Validate each task's predictions
    for tid, expected_count in expected_tasks.items():
        if tid not in submission:
            continue
        pred_list = submission[tid]
        if not isinstance(pred_list, list):
            errors.append(f"Task {tid}: predictions must be a list, got {type(pred_list).__name__}")
            continue

        if len(pred_list) != expected_count:
            errors.append(f"Task {tid}: expected {expected_count} test input predictions, got {len(pred_list)}")

        for p_idx, pred_item in enumerate(pred_list):
            if not isinstance(pred_item, dict):
                errors.append(f"Task {tid}[{p_idx}]: prediction must be a dict, got {type(pred_item).__name__}")
                continue

            for attempt_key in ["attempt_1", "attempt_2"]:
                if attempt_key not in pred_item:
                    errors.append(f"Task {tid}[{p_idx}]: missing required key '{attempt_key}'")
                    continue

                grid = pred_item[attempt_key]
                if not isinstance(grid, list) or len(grid) == 0:
                    errors.append(f"Task {tid}[{p_idx}].{attempt_key}: must be a non-empty 2D list")
                    continue

                h = len(grid)
                if not isinstance(grid[0], list) or len(grid[0]) == 0:
                    errors.append(f"Task {tid}[{p_idx}].{attempt_key}: first row must be a non-empty list")
                    continue

                w = len(grid[0])
                if h > 30 or w > 30:
                    errors.append(f"Task {tid}[{p_idx}].{attempt_key}: dimensions {h}x{w} exceed maximum allowed 30x30")

                for r_idx, row in enumerate(grid):
                    if not isinstance(row, list) or len(row) != w:
                        errors.append(f"Task {tid}[{p_idx}].{attempt_key}: Ragged grid! Row {r_idx} len != expected width {w}")
                        break
                    for c_idx, cell in enumerate(row):
                        if not isinstance(cell, int) or isinstance(cell, bool):
                            errors.append(f"Task {tid}[{p_idx}].{attempt_key}: cell ({r_idx}, {c_idx}) is not an int")
                            break
                        if cell < 0 or cell > 9:
                            errors.append(f"Task {tid}[{p_idx}].{attempt_key}: cell ({r_idx}, {c_idx}) value {cell} out of range [0, 9]")
                            break

    is_valid = len(errors) == 0
    return is_valid, errors
