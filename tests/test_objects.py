"""Tests for src/arc_solver/objects.py - Connected components and object reasoning."""

import pytest
from src.arc_solver.objects import (
    find_objects,
    object_bounding_box,
    crop_object,
    render_objects,
    ObjectEntity,
)

def test_find_objects_4_conn():
    # Grid with 2 distinct objects on background 0
    g = [
        [1, 1, 0, 2],
        [1, 0, 0, 2],
        [0, 0, 0, 2],
    ]
    objs = find_objects(g, background=0, connectivity=4)
    assert len(objs) == 2
    # Verify sizes
    sizes = sorted(o.size for o in objs)
    assert sizes == [3, 3]

def test_find_objects_diagonal_8_conn():
    # Two cells touching only diagonally
    g = [
        [1, 0],
        [0, 1],
    ]
    objs_4 = find_objects(g, background=0, connectivity=4)
    assert len(objs_4) == 2
    objs_8 = find_objects(g, background=0, connectivity=8)
    assert len(objs_8) == 1
    assert objs_8[0].size == 2

def test_object_bounding_box_and_crop():
    g = [
        [0, 0, 0, 0],
        [0, 3, 3, 0],
        [0, 3, 0, 0],
        [0, 0, 0, 0],
    ]
    objs = find_objects(g, background=0, connectivity=4)
    assert len(objs) == 1
    o = objs[0]
    assert o.bbox == (1, 1, 2, 2)
    assert o.height == 2
    assert o.width == 2
    cropped = crop_object(o, background=0)
    assert cropped == [[3, 3], [3, 0]]

def test_render_objects():
    g = [
        [0, 0, 0],
        [0, 4, 0],
        [0, 0, 0],
    ]
    objs = find_objects(g, background=0)
    assert len(objs) == 1
    # Move object down 1 row
    moved = objs[0].translate(1, 0)
    rendered = render_objects([moved], h=3, w=3, background=0)
    assert rendered == [
        [0, 0, 0],
        [0, 0, 0],
        [0, 4, 0],
    ]
