"""Tests for src/arc_solver/solver.py - Multi-family ARC-AGI solver engine."""

import pytest
from src.arc_solver.solver import ARCSolver, CandidateRule

def test_solver_identity_task():
    # Demonstration pairs where output == input
    task = {
        "train": [
            {"input": [[1, 2], [3, 4]], "output": [[1, 2], [3, 4]]},
            {"input": [[5, 6], [7, 8]], "output": [[5, 6], [7, 8]]},
        ],
        "test": [
            {"input": [[9, 0], [1, 2]]}
        ]
    }
    solver = ARCSolver()
    predictions = solver.solve_task(task)
    assert len(predictions) == 1
    p = predictions[0]
    assert "attempt_1" in p and "attempt_2" in p
    assert p["attempt_1"] == [[9, 0], [1, 2]]

def test_solver_d4_rot90_task():
    task = {
        "train": [
            {"input": [[1, 2], [3, 4]], "output": [[3, 1], [4, 2]]},
            {"input": [[5, 6], [7, 8]], "output": [[7, 5], [8, 6]]},
        ],
        "test": [
            {"input": [[0, 1], [2, 3]]}
        ]
    }
    solver = ARCSolver()
    predictions = solver.solve_task(task)
    assert predictions[0]["attempt_1"] == [[2, 0], [3, 1]]

def test_solver_color_remapping():
    task = {
        "train": [
            {"input": [[1, 1], [2, 2]], "output": [[5, 5], [6, 6]]},
            {"input": [[2, 1], [1, 2]], "output": [[6, 5], [5, 6]]},
        ],
        "test": [
            {"input": [[1, 2], [2, 1]]}
        ]
    }
    solver = ARCSolver()
    predictions = solver.solve_task(task)
    assert predictions[0]["attempt_1"] == [[5, 6], [6, 5]]

def test_solver_crop_to_content():
    task = {
        "train": [
            {"input": [[0, 0, 0], [0, 4, 0], [0, 0, 0]], "output": [[4]]},
            {"input": [[0, 0, 0, 0], [0, 4, 4, 0], [0, 0, 0, 0]], "output": [[4, 4]]},
        ],
        "test": [
            {"input": [[0, 0, 0], [0, 2, 2], [0, 2, 2]]}
        ]
    }
    solver = ARCSolver()
    predictions = solver.solve_task(task)
    assert predictions[0]["attempt_1"] == [[2, 2], [2, 2]]

def test_solver_pass2_diversity():
    # Solver provides two distinct attempts when candidates exist
    task = {
        "train": [
            {"input": [[1, 2], [3, 4]], "output": [[1, 2], [3, 4]]},
        ],
        "test": [
            {"input": [[5, 6], [7, 8]]}
        ]
    }
    solver = ARCSolver()
    predictions = solver.solve_task(task)
    p = predictions[0]
    assert p["attempt_1"] == [[5, 6], [7, 8]]
    # Ensure attempt_2 is also a valid 2D grid
    assert isinstance(p["attempt_2"], list)
    assert len(p["attempt_2"]) > 0
