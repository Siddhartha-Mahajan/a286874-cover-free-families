#!/usr/bin/env python3
"""Certify the construction and exact chain arithmetic proving a(17)=68."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from math import comb, floor

from common import PACKAGE, parse_construction, rho, verify_construction, write_json


def main() -> None:
    witness_path = PACKAGE / "constructions/a17_68.txt"
    verification = verify_construction(witness_path)
    n, claimed, words = parse_construction(witness_path)
    vectors = [int(word, 2) for word in words]
    triple_masks = set()
    for vector in vectors:
        points = [i for i in range(n) if vector & (1 << i)]
        for triple in combinations(points, 3):
            triple_masks.add(sum(1 << point for point in triple))

    masses = {w: rho(17, w) for w in range(1, 18)}
    minimum = min(masses.values())
    certificate = {
        "claim": "A286874(17)=68",
        "construction": verification,
        "construction_is_S_3_5_17": (
            verification["valid"]
            and claimed == 68
            and all(word.count("1") == 5 for word in words)
            and len(triple_masks) == comb(17, 3)
            and 68 * comb(5, 3) == comb(17, 3)
        ),
        "distinct_construction_triples": len(triple_masks),
        "rho_by_weight": {str(w): str(value) for w, value in masses.items()},
        "minimum_rho": str(minimum),
        "minimum_weights": [w for w, value in masses.items() if value == minimum],
        "chain_upper_bound": floor(Fraction(1) / minimum),
        "proved": verification["valid"] and minimum == Fraction(1, 68),
    }
    if not certificate["proved"] or not certificate["construction_is_S_3_5_17"]:
        raise AssertionError("a(17)=68 certificate failed")
    write_json(PACKAGE / "certificates/a17_exact.json", certificate)
    print("certified A286874(17)=68")


if __name__ == "__main__":
    main()
