"""
src/arc_solver/grid.py - Grid representation, spatial transformations, and matrix geometry.
"""

from collections import Counter
from typing import Dict, List, Set, Tuple

Grid = List[List[int]]

def dims(g: Grid) -> Tuple[int, int]:
    """Return (height, width) of the grid."""
    if not g:
        return 0, 0
    return len(g), len(g[0])

def same_grid(a: Grid, b: Grid) -> bool:
    """Return True if grids are identical."""
    return a == b

def clone_grid(g: Grid) -> Grid:
    """Return a deep copy of a 2D grid."""
    return [row[:] for row in g]

def new_grid(h: int, w: int, fill: int = 0) -> Grid:
    """Create a new h x w grid initialized to fill color."""
    return [[fill] * w for _ in range(h)]

def rot90(g: Grid) -> Grid:
    """Rotate 90 degrees clockwise."""
    return [list(r) for r in zip(*g[::-1])]

def rot180(g: Grid) -> Grid:
    """Rotate 180 degrees."""
    return [row[::-1] for row in g[::-1]]

def rot270(g: Grid) -> Grid:
    """Rotate 270 degrees clockwise."""
    return [list(r) for r in zip(*g)][::-1]

def flip_h(g: Grid) -> Grid:
    """Flip horizontally (mirror left-to-right)."""
    return [row[::-1] for row in g]

def flip_v(g: Grid) -> Grid:
    """Flip vertically (mirror top-to-bottom)."""
    return g[::-1]

def transpose(g: Grid) -> Grid:
    """Matrix transpose (reflect along main diagonal)."""
    return [list(r) for r in zip(*g)]

def anti_transpose(g: Grid) -> Grid:
    """Anti-diagonal transpose."""
    return rot180([list(r) for r in zip(*g)])

def get_d4_transforms(g: Grid) -> List[Tuple[str, Grid]]:
    """Return the 8 transforms of the dihedral D4 group."""
    return [
        ("identity", clone_grid(g)),
        ("rot90", rot90(g)),
        ("rot180", rot180(g)),
        ("rot270", rot270(g)),
        ("flip_h", flip_h(g)),
        ("flip_v", flip_v(g)),
        ("transpose", transpose(g)),
        ("anti_transpose", anti_transpose(g)),
    ]

def scale_grid(g: Grid, factor_h: int, factor_w: int) -> Grid:
    """Scale each cell into a factor_h x factor_w block."""
    out = []
    for row in g:
        expanded_row = [val for val in row for _ in range(factor_w)]
        for _ in range(factor_h):
            out.append(expanded_row[:])
    return out

def tile_grid(g: Grid, repeat_h: int, repeat_w: int) -> Grid:
    """Tile the grid repeat_h times vertically and repeat_w times horizontally."""
    wide = [row * repeat_w for row in g]
    out = []
    for _ in range(repeat_h):
        for r in wide:
            out.append(r[:])
    return out

def crop_grid(g: Grid, r0: int, c0: int, h: int, w: int) -> Grid:
    """Extract a subgrid starting at (r0, c0) with dimensions (h, w)."""
    return [row[c0:c0 + w] for row in g[r0:r0 + h]]

def get_colors(g: Grid) -> Set[int]:
    """Return set of distinct colors present in grid."""
    return {val for row in g for val in row}

def get_color_counts(g: Grid) -> Dict[int, int]:
    """Return frequency mapping of colors in grid."""
    return Counter(val for row in g for val in row)

def get_background_color(g: Grid) -> int:
    """
    Infer background color as the most frequent color.
    In case of ties, choose the lower integer color code deterministically.
    """
    counts = get_color_counts(g)
    if not counts:
        return 0
    # Sort primarily by descending count (-v), secondarily by ascending color (k)
    return min(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0]
