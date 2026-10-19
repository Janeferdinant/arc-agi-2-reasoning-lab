"""
src/arc_solver/objects.py - Connected component analysis and object-centric reasoning.
"""

from typing import Dict, List, Optional, Set, Tuple
from src.arc_solver.grid import Grid, dims, new_grid

class ObjectEntity:
    """Represents a discrete connected object within an ARC grid."""
    def __init__(self, cells: Dict[Tuple[int, int], int]):
        self.cells = dict(cells)  # (r, c) -> color
        if not self.cells:
            self.bbox = (0, 0, 0, 0)
            self.height = 0
            self.width = 0
            self.size = 0
            self.colors = set()
            return

        rs = [r for r, _ in self.cells]
        cs = [c for _, c in self.cells]
        self.bbox = (min(rs), min(cs), max(rs), max(cs))  # min_r, min_c, max_r, max_c
        self.height = self.bbox[2] - self.bbox[0] + 1
        self.width = self.bbox[3] - self.bbox[1] + 1
        self.size = len(self.cells)
        self.colors = set(self.cells.values())

    @property
    def is_solid(self) -> bool:
        """True if the object completely fills its bounding box."""
        return self.size == (self.height * self.width)

    def translate(self, dr: int, dc: int) -> "ObjectEntity":
        """Return a new ObjectEntity shifted by (dr, dc)."""
        new_cells = {(r + dr, c + dc): col for (r, c), col in self.cells.items()}
        return ObjectEntity(new_cells)

    def recolor(self, new_color: int) -> "ObjectEntity":
        """Return a new ObjectEntity where all cells are set to new_color."""
        new_cells = {pos: new_color for pos in self.cells}
        return ObjectEntity(new_cells)

def _get_neighbors(r: int, c: int, h: int, w: int, connectivity: int = 4) -> List[Tuple[int, int]]:
    """Return valid in-bounds neighbors for a cell."""
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if connectivity == 8:
        deltas += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    neighbors = []
    for dr, dc in deltas:
        nr, nc = r + dr, c + dc
        if 0 <= nr < h and 0 <= nc < w:
            neighbors.append((nr, nc))
    return neighbors

def find_objects(
    g: Grid,
    background: int = 0,
    connectivity: int = 4,
    by_color: bool = False
) -> List[ObjectEntity]:
    """
    Find connected components of non-background cells.
    If by_color is True, cells must share the same color to be connected.
    Returns list of ObjectEntity sorted deterministically (top-left scan order).
    """
    h, w = dims(g)
    visited = [[False] * w for _ in range(h)]
    entities: List[ObjectEntity] = []

    for r in range(h):
        for c in range(w):
            if visited[r][c] or g[r][c] == background:
                continue

            target_color = g[r][c] if by_color else None
            component_cells: Dict[Tuple[int, int], int] = {}
            queue = [(r, c)]
            visited[r][c] = True

            while queue:
                cr, cc = queue.pop(0)
                component_cells[(cr, cc)] = g[cr][cc]

                for nr, nc in _get_neighbors(cr, cc, h, w, connectivity):
                    if not visited[nr][nc] and g[nr][nc] != background:
                        if not by_color or g[nr][nc] == target_color:
                            visited[nr][nc] = True
                            queue.append((nr, nc))

            if component_cells:
                entities.append(ObjectEntity(component_cells))

    # Sort deterministically by top-left bounding box coordinates
    entities.sort(key=lambda o: (o.bbox[0], o.bbox[1]))
    return entities

def object_bounding_box(obj: ObjectEntity) -> Tuple[int, int, int, int]:
    """Return (min_r, min_c, max_r, max_c)."""
    return obj.bbox

def crop_object(obj: ObjectEntity, background: int = 0) -> Grid:
    """Extract and return the minimal bounding-box subgrid containing the object."""
    min_r, min_c, max_r, max_c = obj.bbox
    out = new_grid(obj.height, obj.width, fill=background)
    for (r, c), color in obj.cells.items():
        out[r - min_r][c - min_c] = color
    return out

def render_objects(
    objects: List[ObjectEntity],
    h: int,
    w: int,
    background: int = 0
) -> Grid:
    """Render a list of ObjectEntities onto an h x w canvas with given background."""
    out = new_grid(h, w, fill=background)
    for obj in objects:
        for (r, c), color in obj.cells.items():
            if 0 <= r < h and 0 <= c < w:
                out[r][c] = color
    return out
