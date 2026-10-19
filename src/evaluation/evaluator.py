"""
src/evaluation/evaluator.py - Exact match and Pass@2 evaluation framework for ARC-AGI-2.
"""

import time
from typing import Any, Dict, List, Optional
from src.arc_solver.grid import Grid, same_grid
from src.arc_solver.solver import ARCSolver

def evaluate_predictions(
    predictions: List[Dict[str, Grid]],
    ground_truth: List[Grid]
) -> Dict[str, Any]:
    """
    Evaluate solver predictions against ground truth for a single task.
    Returns dictionary with task-level pass_1, pass_2, and input-level counts.
    """
    total_inputs = len(ground_truth)
    if len(predictions) != total_inputs:
        return {
            "pass_1": False,
            "pass_2": False,
            "test_inputs_total": total_inputs,
            "test_inputs_correct_pass1": 0,
            "test_inputs_correct_pass2": 0,
            "error": f"Prediction count {len(predictions)} != ground truth count {total_inputs}"
        }

    correct_p1_count = 0
    correct_p2_count = 0

    for pred, true_grid in zip(predictions, ground_truth):
        att1 = pred.get("attempt_1")
        att2 = pred.get("attempt_2")

        p1_match = att1 is not None and same_grid(att1, true_grid)
        p2_match = p1_match or (att2 is not None and same_grid(att2, true_grid))

        if p1_match:
            correct_p1_count += 1
        if p2_match:
            correct_p2_count += 1

    return {
        "pass_1": correct_p1_count == total_inputs,
        "pass_2": correct_p2_count == total_inputs,
        "test_inputs_total": total_inputs,
        "test_inputs_correct_pass1": correct_p1_count,
        "test_inputs_correct_pass2": correct_p2_count,
    }

def evaluate_dataset_subset(
    challenges: Dict[str, Any],
    solutions: Dict[str, List[Grid]],
    solver: Optional[ARCSolver] = None,
    task_ids: Optional[List[str]] = None,
    max_tasks: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Evaluate solver across a set of tasks.
    Returns aggregate accuracy, Pass@1, Pass@2, latency, and detailed task reports.
    """
    if solver is None:
        solver = ARCSolver()

    target_ids = task_ids or list(challenges.keys())
    if max_tasks is not None:
        target_ids = target_ids[:max_tasks]

    start_time = time.perf_counter()
    task_results = {}
    tasks_solved_p1 = 0
    tasks_solved_p2 = 0
    total_inputs_evaluated = 0
    inputs_correct_p1 = 0
    inputs_correct_p2 = 0

    for tid in target_ids:
        if tid not in challenges or tid not in solutions:
            continue

        task_data = challenges[tid]
        ground_truth = solutions[tid]

        t0 = time.perf_counter()
        predictions = solver.solve_task(task_data)
        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        eval_res = evaluate_predictions(predictions, ground_truth)
        eval_res["latency_ms"] = elapsed_ms
        task_results[tid] = eval_res

        if eval_res["pass_1"]:
            tasks_solved_p1 += 1
        if eval_res["pass_2"]:
            tasks_solved_p2 += 1

        total_inputs_evaluated += eval_res["test_inputs_total"]
        inputs_correct_p1 += eval_res["test_inputs_correct_pass1"]
        inputs_correct_p2 += eval_res["test_inputs_correct_pass2"]

    total_time_sec = time.perf_counter() - start_time
    total_tasks = len(task_results)

    return {
        "total_tasks": total_tasks,
        "tasks_solved_pass1": tasks_solved_p1,
        "tasks_solved_pass2": tasks_solved_p2,
        "task_accuracy_pass1": round(tasks_solved_p1 / total_tasks, 4) if total_tasks else 0.0,
        "task_accuracy_pass2": round(tasks_solved_p2 / total_tasks, 4) if total_tasks else 0.0,
        "total_inputs": total_inputs_evaluated,
        "inputs_correct_pass1": inputs_correct_p1,
        "inputs_correct_pass2": inputs_correct_p2,
        "input_accuracy_pass1": round(inputs_correct_p1 / total_inputs_evaluated, 4) if total_inputs_evaluated else 0.0,
        "input_accuracy_pass2": round(inputs_correct_p2 / total_inputs_evaluated, 4) if total_inputs_evaluated else 0.0,
        "total_duration_sec": round(total_time_sec, 3),
        "avg_latency_ms_per_task": round((total_time_sec / total_tasks * 1000.0), 2) if total_tasks else 0.0,
        "task_results": task_results,
    }
