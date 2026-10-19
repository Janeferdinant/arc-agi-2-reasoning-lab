"""Tests for src/arc_solver/grid.py - Grid representation and geometry."""

import pytest
from src.arc_solver.grid import (
    dims,
    same_grid,
    clone_grid,
    rot90,
    rot180,
    rot270,
    flip_h,
    flip_v,
    transpose,
    anti_transpose,
    get_d4_transforms,
    scale_grid,
    tile_grid,
    crop_grid,
    get_colors,
    get_color_counts,
    get_background_color,
)

def test_grid_dims_and_clone():
    g = [[1, 2, 3], [4, 5, 6]]
    assert dims(g) == (2, 3)
    c = clone_grid(g)
    assert c == g
    assert c is not g
    c[0][0] = 9
    assert g[0][0] == 1  # Verify deep copy

def test_rotations_and_reflections():
    g = [[1, 2], [3, 4]]
    # rot90 clockwise: [[3, 1], [4, 2]]
    assert rot90(g) == [[3, 1], [4, 2]]
    # rot180: [[4, 3], [2, 1]]
    assert rot180(g) == [[4, 3], [2, 1]]
    # rot270: [[2, 4], [1, 3]]
    assert rot270(g) == [[2, 4], [1, 3]]
    # flip_h (horizontal mirror - flip rows across vertical axis)
    assert flip_h(g) == [[2, 1], [4, 3]]
    # flip_v (vertical mirror - flip columns across horizontal axis)
    assert flip_v(g) == [[3, 4], [1, 2]]
    # transpose: [[1, 3], [2, 4]]
    assert transpose(g) == [[1, 3], [2, 4]]
    # anti_transpose: [[4, 2], [3, 1]]
    assert anti_transpose(g) == [[4, 2], [3, 1]]

def test_d4_group_has_8_transforms():
    g = [[1, 2], [3, 4]]
    d4 = get_d4_transforms(g)
    assert len(d4) == 8
    assert ("identity", g) in d4

def test_scale_and_tile():
    g = [[1, 2], [3, 4]]
    s2 = scale_grid(g, 2, 2)
    assert dims(s2) == (4, 4)
    assert s2[0] == [1, 1, 2, 2]
    assert s2[2] == [3, 3, 4, 4]
    
    t = tile_grid(g, 2, 3)
    assert dims(t) == (4, 6)

def test_crop_and_palette():
    g = [[0, 0, 0], [0, 5, 0], [0, 5, 5]]
    cropped = crop_grid(g, 1, 1, 2, 2)
    assert cropped == [[5, 0], [5, 5]]
    assert get_colors(g) == {0, 5}
    counts = get_color_counts(g)
    assert counts[0] == 6
    assert counts[5] == 3
    assert get_background_color(g) == 0
