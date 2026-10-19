"""Tests for src/arc_solver/transforms.py - Domain Specific Language transforms."""

import pytest
from src.arc_solver.transforms import (
    remap_colors,
    apply_gravity,
    crop_to_content,
    complete_symmetry,
    fill_enclosed_holes,
)

def test_remap_colors():
    g = [[1, 2], [3, 1]]
    mapping = {1: 7, 2: 8, 3: 9}
    res = remap_colors(g, mapping)
    assert res == [[7, 8], [9, 7]]

def test_apply_gravity_down():
    # Floating block drops to bottom
    g = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]
    dropped = apply_gravity(g, direction="down", background=0)
    assert dropped == [
        [0, 0, 0],
        [0, 1, 0],
        [0, 1, 0],
    ]

def test_crop_to_content():
    g = [
        [0, 0, 0, 0],
        [0, 2, 2, 0],
        [0, 0, 0, 0],
    ]
    cropped = crop_to_content(g, background=0)
    assert cropped == [[2, 2]]

def test_complete_symmetry_vertical():
    # Left half given, mirror to right
    g = [
        [1, 0, 0, 0],
        [0, 2, 0, 0],
    ]
    mirrored = complete_symmetry(g, axis="vertical", background=0)
    assert mirrored == [
        [1, 0, 0, 1],
        [0, 2, 2, 0],
    ]

def test_fill_enclosed_holes():
    # A 3x3 square frame with a hole in the center
    g = [
        [5, 5, 5],
        [5, 0, 5],
        [5, 5, 5],
    ]
    filled = fill_enclosed_holes(g, fill_color=3, background=0)
    assert filled == [
        [5, 5, 5],
        [5, 3, 5],
        [5, 5, 5],
    ]
