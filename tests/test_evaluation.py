"""Tests for src/evaluation/evaluator.py - Exact match and Pass@2 evaluation."""

import pytest
from src.evaluation.evaluator import evaluate_predictions, evaluate_dataset_subset

def test_evaluate_predictions_pass1_and_pass2():
    # Ground truth: list of expected grids for test inputs
    ground_truth = [[[1, 2], [3, 4]]]
    
    # Case 1: attempt 1 correct
    preds_p1 = [{"attempt_1": [[1, 2], [3, 4]], "attempt_2": [[0, 0], [0, 0]]}]
    res1 = evaluate_predictions(preds_p1, ground_truth)
    assert res1["pass_1"] is True
    assert res1["pass_2"] is True

    # Case 2: attempt 2 correct (Pass@2 success, Pass@1 fail)
    preds_p2 = [{"attempt_1": [[9, 9], [9, 9]], "attempt_2": [[1, 2], [3, 4]]}]
    res2 = evaluate_predictions(preds_p2, ground_truth)
    assert res2["pass_1"] is False
    assert res2["pass_2"] is True

    # Case 3: both wrong
    preds_fail = [{"attempt_1": [[0, 0]], "attempt_2": [[1, 1]]}]
    res3 = evaluate_predictions(preds_fail, ground_truth)
    assert res3["pass_1"] is False
    assert res3["pass_2"] is False

def test_multi_input_task_requires_all_solved():
    # Task with 2 test inputs
    ground_truth = [
        [[1]],
        [[2]]
    ]
    # One correct, one wrong -> task overall is NOT solved
    preds_partial = [
        {"attempt_1": [[1]], "attempt_2": [[0]]},
        {"attempt_1": [[0]], "attempt_2": [[0]]},
    ]
    res = evaluate_predictions(preds_partial, ground_truth)
    assert res["pass_1"] is False
    assert res["pass_2"] is False
    assert res["test_inputs_correct_pass2"] == 1
    assert res["test_inputs_total"] == 2
