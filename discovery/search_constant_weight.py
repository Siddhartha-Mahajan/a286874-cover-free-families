#!/usr/bin/env python3
"""Search for strong constant-weight lower bounds for A286874.

For weight w and maximum pairwise intersection t with w > 2t, every
selected word has a coordinate outside the union of every other pair.
Thus every solution written by this program is a rigorously valid lower
bound, independently checkable by verify_constructions.py.
"""

from __future__ import annotations

import argparse
import itertools
import re
from pathlib import Path

from ortools.sat.python import cp_model


def subsets_as_masks(n: int, size: int) -> list[int]:
    return [sum(1 << i for i in subset) for subset in itertools.combinations(range(n), size)]


def bits(mask: int, n: int) -> str:
    return format(mask, f"0{n}b")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    parser.add_argument("--weight", type=int, default=5)
    parser.add_argument("--intersection", type=int, default=2)
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--hint", type=Path)
    parser.add_argument("--minimum", type=int)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.weight <= 2 * args.intersection:
        raise SystemExit("need weight > 2*intersection for the cover-free proof")

    candidates = subsets_as_masks(args.n, args.weight)
    forbidden_size = args.intersection + 1
    containers: dict[int, list[int]] = {mask: [] for mask in subsets_as_masks(args.n, forbidden_size)}
    for i, candidate in enumerate(candidates):
        for subset in itertools.combinations([b for b in range(args.n) if candidate >> b & 1], forbidden_size):
            containers[sum(1 << b for b in subset)].append(i)

    model = cp_model.CpModel()
    chosen = [model.new_bool_var(f"x_{mask}") for mask in candidates]
    for indices in containers.values():
        model.add(sum(chosen[i] for i in indices) <= 1)
    if args.minimum is not None:
        model.add(sum(chosen) >= args.minimum)
    if args.hint:
        hint_masks = {
            int(word, 2)
            for word in re.findall(rf"\b[01]{{{args.n}}}\b", args.hint.read_text())
            if word.count("1") == args.weight
        }
        # Only hint the selected blocks.  Leaving all other variables unset lets
        # CP-SAT extend or repair the construction when --minimum is larger.
        candidate_index = {mask: i for i, mask in enumerate(candidates)}
        for mask in hint_masks:
            if mask in candidate_index:
                model.add_hint(chosen[candidate_index[mask]], 1)
        print(f"hinted_vectors={len(hint_masks)}")
    model.maximize(sum(chosen))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    solver.parameters.log_search_progress = True
    status = solver.solve(model)
    selected = [mask for mask, var in zip(candidates, chosen) if solver.boolean_value(var)]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        f"a({args.n}) >= {len(selected)}:\n"
        + "\n".join(bits(mask, args.n) for mask in selected)
        + "\n"
    )
    print(f"status={solver.status_name(status)}")
    print(f"objective={solver.objective_value}")
    print(f"best_bound={solver.best_objective_bound}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
