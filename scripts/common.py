#!/usr/bin/env python3
"""Shared exact arithmetic, parsing, and verification for the final package."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
from math import comb
from pathlib import Path
import re


PACKAGE = Path(__file__).resolve().parents[1]
HEADER = re.compile(r"a\((\d+)\)\s*>=\s*(\d+):")


def mu(n: int, w: int, s: int) -> Fraction:
    if s == w:
        return Fraction(1, comb(n, w))
    return Fraction(n - w, n - s) / comb(n, s)


def rho(n: int, w: int) -> Fraction:
    """Minimum private-subset random-chain mass for a member of weight w."""
    if w % 2:
        threshold = (w + 1) // 2
        return sum(
            (comb(w, s) * mu(n, w, s) for s in range(threshold, w + 1)),
            Fraction(0),
        )
    threshold = w // 2
    return (
        Fraction(comb(w, threshold), 2) * mu(n, w, threshold)
        + sum(
            (comb(w, s) * mu(n, w, s) for s in range(threshold + 1, w + 1)),
            Fraction(0),
        )
    )


def parse_construction(path: Path) -> tuple[int, int, list[str]]:
    text = path.read_text()
    match = HEADER.search(text)
    if not match:
        raise ValueError(f"missing construction header in {path}")
    n, claimed = map(int, match.groups())
    words = [
        word
        for word in re.findall(r"\b[01]+\b", text[match.end() :])
        if len(word) == n
    ]
    return n, claimed, words


def verify_construction(path: Path) -> dict[str, object]:
    n, claimed, words = parse_construction(path)
    vectors = [int(word, 2) for word in words]
    counterexample = None
    if len(words) == claimed and len(set(words)) == len(words):
        for target_index, target in enumerate(vectors):
            others = [i for i in range(len(vectors)) if i != target_index]
            for first, second in itertools.combinations(others, 2):
                if target & ~(vectors[first] | vectors[second]) == 0:
                    counterexample = [target_index, first, second]
                    break
            if counterexample:
                break
    valid = (
        len(words) == claimed
        and len(set(words)) == len(words)
        and counterexample is None
    )
    intersections = Counter(
        (left & right).bit_count()
        for left, right in itertools.combinations(vectors, 2)
    )
    return {
        "path": str(path.relative_to(PACKAGE)),
        "n": n,
        "claimed": claimed,
        "parsed": len(words),
        "distinct": len(set(words)),
        "weight_histogram": dict(
            sorted(Counter(word.count("1") for word in words).items())
        ),
        "pair_intersection_histogram": dict(sorted(intersections.items())),
        "counterexample": counterexample,
        "valid": valid,
    }


def cover_free_ints(words: tuple[int, ...]) -> bool:
    if len(words) != len(set(words)):
        return False
    for target_index, target in enumerate(words):
        others = [word for i, word in enumerate(words) if i != target_index]
        for first, second in itertools.combinations(others, 2):
            if target & ~(first | second) == 0:
                return False
    return True


def parse_extremals(path: Path) -> list[tuple[int, ...]]:
    families = []
    for line in path.read_text().splitlines():
        match = re.fullmatch(r"\{([0-9a-f ]+)\}", line.strip())
        if match:
            families.append(tuple(int(token, 16) for token in match.group(1).split()))
    return families


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
