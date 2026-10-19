"""
src/arc_solver/solver.py - Multi-family hybrid ARC-AGI-2 reasoning engine.
"""

from typing import Any, Callable, Dict, List, Optional, Tuple
from collections import Counter
from src.arc_solver.grid import (
    Grid,
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
    scale_grid,
    tile_grid,
    get_colors,
    get_background_color,
)
from src.arc_solver.transforms import (
    remap_colors,
    apply_gravity,
    crop_to_content,
    complete_symmetry,
    fill_enclosed_holes,
)

class CandidateRule:
    """Represents a hypothesized transformation rule for ARC tasks."""
    def __init__(
        self,
        name: str,
        family: str,
        priority: int,
        predict_fn: Callable[[Grid], Optional[Grid]],
        complexity: float = 1.0,
    ):
        self.name = name
        self.family = family
        self.priority = priority
        self.predict_fn = predict_fn
        self.complexity = complexity

    def predict(self, g: Grid) -> Optional[Grid]:
        try:
            res = self.predict_fn(g)
            if res is None:
                return None
            h, w = dims(res)
            if h < 1 or w < 1 or h > 30 or w > 30:
                return None
            for row in res:
                if len(row) != w:
                    return None
                for val in row:
                    if not isinstance(val, int) or val < 0 or val > 9:
                        return None
            return res
        except Exception:
            return None

class ARCSolver:
    """Multi-family hybrid symbolic solver with bounded search and Pass@2 ranking."""
    def __init__(self, timeout_sec: float = 2.0):
        self.timeout_sec = timeout_sec

    def generate_candidate_rules(self, train_pairs: List[Dict[str, Grid]]) -> List[CandidateRule]:
        """Generate candidate transformation rules across multiple solver families."""
        rules: List[CandidateRule] = []

        # 1. Constant output rule (only if demonstrations are not already all identity)
        if train_pairs:
            first_out = train_pairs[0]["output"]
            all_same_out = all(same_grid(p["output"], first_out) for p in train_pairs)
            all_identity = all(same_grid(p["input"], p["output"]) for p in train_pairs)
            # Only trigger constant output if it is not purely an identity task
            if all_same_out and not all_identity:
                rules.append(CandidateRule(
                    name="constant_output",
                    family="geometry",
                    priority=1,
                    predict_fn=lambda g, out=first_out: clone_grid(out),
                    complexity=0.5
                ))

        # 2. Geometric D4 transforms (identity, rotations, reflections)
        d4_ops = [
            ("identity", 1, lambda g: clone_grid(g)),
            ("rot90", 2, rot90),
            ("rot180", 2, rot180),
            ("rot270", 2, rot270),
            ("flip_h", 2, flip_h),
            ("flip_v", 2, flip_v),
            ("transpose", 3, transpose),
            ("anti_transpose", 3, anti_transpose),
        ]
        for op_name, prio, fn in d4_ops:
            rules.append(CandidateRule(
                name=f"d4_{op_name}",
                family="geometry",
                priority=prio,
                predict_fn=fn,
                complexity=float(prio)
            ))

        # 3. Global Color Remapping
        color_mapping: Dict[int, int] = {}
        mapping_valid = True
        for p in train_pairs:
            gi, go = p["input"], p["output"]
            if dims(gi) != dims(go):
                mapping_valid = False
                break
            for ri, ro in zip(gi, go):
                for vi, vo in zip(ri, ro):
                    if color_mapping.setdefault(vi, vo) != vo:
                        mapping_valid = False
                        break
                if not mapping_valid:
                    break
            if not mapping_valid:
                break

        if mapping_valid and color_mapping:
            def predict_color_map(g, m=color_mapping):
                # Reject if any color in g has no established mapping
                for row in g:
                    for val in row:
                        if val not in m:
                            return None
                return remap_colors(g, m)

            rules.append(CandidateRule(
                name="color_remapping",
                family="color",
                priority=2,
                predict_fn=predict_color_map,
                complexity=2.0
            ))

        # 4. Scaling (2x2, 3x3)
        for factor in [2, 3]:
            rules.append(CandidateRule(
                name=f"scale_{factor}x{factor}",
                family="scale_tile",
                priority=3,
                predict_fn=lambda g, f=factor: scale_grid(g, f, f),
                complexity=3.0
            ))

        # 5. Tiling
        for th in [1, 2, 3]:
            for tw in [1, 2, 3]:
                if th == 1 and tw == 1:
                    continue
                rules.append(CandidateRule(
                    name=f"tile_{th}x{tw}",
                    family="scale_tile",
                    priority=4,
                    predict_fn=lambda g, h_rep=th, w_rep=tw: tile_grid(g, h_rep, w_rep),
                    complexity=4.0
                ))

        # 6. Object-Centric Crop
        for margin in [0, 1]:
            rules.append(CandidateRule(
                name=f"crop_content_m{margin}",
                family="object_spatial",
                priority=3,
                predict_fn=lambda g, m=margin: crop_to_content(g, background=get_background_color(g), margin=m),
                complexity=2.5
            ))

        # 7. Gravity simulation in 4 directions
        for d in ["down", "up", "left", "right"]:
            rules.append(CandidateRule(
                name=f"gravity_{d}",
                family="object_spatial",
                priority=4,
                predict_fn=lambda g, direction=d: apply_gravity(g, direction=direction, background=get_background_color(g)),
                complexity=3.5
            ))

        # 8. Symmetry Completion
        for axis in ["vertical", "horizontal"]:
            rules.append(CandidateRule(
                name=f"symmetry_{axis}",
                family="object_spatial",
                priority=4,
                predict_fn=lambda g, ax=axis: complete_symmetry(g, axis=ax, background=get_background_color(g)),
                complexity=3.5
            ))

        # 9. Hole filling
        # Collect candidate fill colors from outputs
        output_colors = {val for p in train_pairs for row in p["output"] for val in row}
        for fc in output_colors:
            rules.append(CandidateRule(
                name=f"fill_holes_c{fc}",
                family="object_spatial",
                priority=5,
                predict_fn=lambda g, col=fc: fill_enclosed_holes(g, fill_color=col, background=get_background_color(g)),
                complexity=4.0
            ))

        return rules

    def find_consistent_rules(
        self,
        train_pairs: List[Dict[str, Grid]]
    ) -> List[CandidateRule]:
        """Filter candidate rules to those that explain 100% of demonstration pairs."""
        candidates = self.generate_candidate_rules(train_pairs)
        consistent_rules: List[CandidateRule] = []

        for rule in candidates:
            all_match = True
            for pair in train_pairs:
                pred = rule.predict(pair["input"])
                if pred is None or not same_grid(pred, pair["output"]):
                    all_match = False
                    break
            if all_match:
                consistent_rules.append(rule)

        # Sort consistent rules by priority (ascending) and complexity
        consistent_rules.sort(key=lambda r: (r.priority, r.complexity))
        return consistent_rules

    def solve_test_input(
        self,
        test_input: Grid,
        consistent_rules: List[CandidateRule],
        train_pairs: List[Dict[str, Grid]]
    ) -> Dict[str, Grid]:
        """Generate attempt_1 and attempt_2 predictions for a single test input."""
        candidate_predictions: List[Grid] = []

        for rule in consistent_rules:
            pred = rule.predict(test_input)
            if pred is not None and not any(same_grid(pred, existing) for existing in candidate_predictions):
                candidate_predictions.append(pred)

        # Attempt 1: best matching candidate
        if candidate_predictions:
            attempt_1 = candidate_predictions[0]
        else:
            # Fallback 1: identity or cropped
            attempt_1 = clone_grid(test_input)

        # Attempt 2: second distinct candidate or principled variation
        if len(candidate_predictions) >= 2:
            attempt_2 = candidate_predictions[1]
        else:
            # Generate diverse alternative
            # If attempt_1 is identity, try crop; if crop, try rot90
            bg = get_background_color(test_input)
            cropped = crop_to_content(test_input, background=bg)
            if not same_grid(cropped, attempt_1):
                attempt_2 = cropped
            else:
                r90 = rot90(test_input)
                attempt_2 = r90 if not same_grid(r90, attempt_1) else clone_grid(test_input)

        return {
            "attempt_1": attempt_1,
            "attempt_2": attempt_2,
        }

    def solve_task(self, task: Dict[str, Any]) -> List[Dict[str, Grid]]:
        """
        Solve an entire task with its demonstration pairs and test inputs.
        Returns list of {'attempt_1': Grid, 'attempt_2': Grid} for each test query.
        """
        train_pairs = task.get("train", [])
        test_queries = task.get("test", [])
        consistent_rules = self.find_consistent_rules(train_pairs)

        results = []
        for t_query in test_queries:
            t_input = t_query["input"]
            preds = self.solve_test_input(t_input, consistent_rules, train_pairs)
            results.append(preds)
        return results
