"""Tests for src/submission/validator.py - Strict Kaggle ARC submission schema validation."""

import pytest
from src.submission.validator import validate_submission_dict

def test_valid_submission():
    sub = {
        "task_1": [
            {"attempt_1": [[1, 2], [3, 4]], "attempt_2": [[0, 0], [0, 0]]}
        ]
    }
    expected_tasks = {"task_1": 1}
    valid, errors = validate_submission_dict(sub, expected_tasks)
    assert valid is True
    assert len(errors) == 0

def test_missing_task_id():
    sub = {
        "task_1": [{"attempt_1": [[0]], "attempt_2": [[0]]}]
    }
    expected_tasks = {"task_1": 1, "task_2": 1}
    valid, errors = validate_submission_dict(sub, expected_tasks)
    assert valid is False
    assert any("Missing task ID" in err for err in errors)

def test_missing_attempt_key():
    sub = {
        "task_1": [{"attempt_1": [[0]]}]  # missing attempt_2
    }
    expected_tasks = {"task_1": 1}
    valid, errors = validate_submission_dict(sub, expected_tasks)
    assert valid is False
    assert any("attempt_2" in err for err in errors)

def test_ragged_grid():
    sub = {
        "task_1": [
            {
                "attempt_1": [[1, 2], [3]],  # Ragged! row 0 has 2 items, row 1 has 1
                "attempt_2": [[0, 0], [0, 0]]
            }
        ]
    }
    expected_tasks = {"task_1": 1}
    valid, errors = validate_submission_dict(sub, expected_tasks)
    assert valid is False
    assert any("Ragged" in err for err in errors)

def test_invalid_color_value():
    sub = {
        "task_1": [
            {
                "attempt_1": [[10]],  # 10 is out of bounds [0, 9]
                "attempt_2": [[0]]
            }
        ]
    }
    expected_tasks = {"task_1": 1}
    valid, errors = validate_submission_dict(sub, expected_tasks)
    assert valid is False
    assert any("out of range" in err for err in errors)
