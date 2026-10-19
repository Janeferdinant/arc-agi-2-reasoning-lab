"""
src/arc_solver/transforms.py - Composable Domain-Specific Language (DSL) transformations.
"""

from collections import deque
from typing import Dict, List, Optional, Tuple
from src.arc_solver.grid import (
    Grid,
    clone_grid,
    dims,
    new_grid,
    crop_grid,
    rot90,
    rot180,
    rot270,
    flip_h,
    flip_v,
)

def remap_colors(g: Grid, mapping: Dict[int, int]) -> Grid:
    """Remap grid cell colors according to mapping dictionary."""
    return [[mapping.get(val, val) for val in row] for row in g]

def apply_gravity(g: Grid, direction: str = "down", background: int = 0) -> Grid:
    """
    Simulate gravity on non-background cells falling in the given direction.
    direction in ['down', 'up', 'left', 'right']
    """
    h, w = dims(g)
    if direction == "down":
        out = new_grid(h, w, fill=background)
        for c in range(w):
            col_vals = [g[r][c] for r in range(h) if g[r][c] != background]
            # Place non-background cells at the bottom
            start_r = h - len(col_vals)
            for idx, val in enumerate(col_vals):
                out[start_r + idx][c] = val
        return out
    elif direction == "up":
        out = new_grid(h, w, fill=background)
        for c in range(w):
            col_vals = [g[r][c] for r in range(h) if g[r][c] != background]
            for idx, val in enumerate(col_vals):
                out[idx][c] = val
        return out
    elif direction == "right":
        out = new_grid(h, w, fill=background)
        for r in range(h):
            row_vals = [g[r][c] for c in range(w) if g[r][c] != background]
            start_c = w - len(row_vals)
            for idx, val in enumerate(row_vals):
                out[r][start_c + idx] = val
        return out
    elif direction == "left":
        out = new_grid(h, w, fill=background)
        for r in range(h):
            row_vals = [g[r][c] for c in range(w) if g[r][c] != background]
            for idx, val in enumerate(row_vals):
                out[r][idx] = val
        return out
    return clone_grid(g)

def crop_to_content(g: Grid, background: int = 0, margin: int = 0) -> Grid:
    """Crop grid to bounding box of all non-background cells."""
    h, w = dims(g)
    rs, cs = [], []
    for r in range(h):
        for c in range(w):
            if g[r][c] != background:
                rs.append(r)
                cs.append(c)
    if not rs:
        return [[background]]
    min_r, max_r = max(0, min(rs) - margin), min(h - 1, max(rs) + margin)
    min_c, max_c = max(0, min(cs) - margin), min(w - 1, max(cs) + margin)
    return crop_grid(g, min_r, min_c, max_r - min_r + 1, max_c - min_c + 1)

def complete_symmetry(g: Grid, axis: str = "vertical", background: int = 0) -> Grid:
    """Complete a partial symmetric pattern along vertical or horizontal axis."""
    h, w = dims(g)
    out = clone_grid(g)
    if axis == "vertical":
        mid = w // 2
        for r in range(h):
            for c in range(mid):
                opp_c = w - 1 - c
                if out[r][c] != background and out[r][opp_c] == background:
                    out[r][opp_c] = out[r][c]
                elif out[r][opp_c] != background and out[r][c] == background:
                    out[r][c] = out[r][opp_c]
    elif axis == "horizontal":
        mid = h // 2
        for r in range(mid):
            opp_r = h - 1 - r
            for c in range(w):
                if out[r][c] != background and out[opp_r][c] == background:
                    out[opp_r][c] = out[r][c]
                elif out[opp_r][c] != background and out[r][c] == background:
                    out[r][c] = out[opp_r][c]
    return out

def fill_enclosed_holes(g: Grid, fill_color: int, background: int = 0) -> Grid:
    """
    Find background cells that cannot reach the grid boundaries through 4-way
    background connectivity (i.e. holes enclosed by foreground walls) and fill them.
    """
    h, w = dims(g)
    reachable = [[False] * w for _ in range(h)]
    queue: deque = deque()

    # Seed with all border cells that are background
    for r in range(h):
        for c in (0, w - 1):
            if g[r][c] == background and not reachable[r][c]:
                reachable[r][c] = True
                queue.append((r, c))
    for c in range(w):
        for r in (0, h - 1):
            if g[r][c] == background and not reachable[r][c]:
                reachable[r][c] = True
                queue.append((r, c))

    while queue:
        cr, cc = queue.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = cr + dr, cc + dc
            if 0 <= nr < h and 0 <= nc < w:
                if g[nr][nc] == background and not reachable[nr][nc]:
                    reachable[nr][nc] = True
                    queue.append((nr, nc))

    out = clone_grid(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] == background and not reachable[r][c]:
                out[r][c] = fill_color
    return out
