#!/usr/bin/env python3
"""Replay every finite certificate used to prove A286874(15)=42."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from math import comb, floor

from common import (
    PACKAGE,
    cover_free_ints,
    mu,
    parse_extremals,
    rho,
    sha256,
    verify_construction,
    write_json,
)


MASK14 = (1 << 14) - 1


def separated(target: int, first: int, second: int) -> bool:
    return bool(target & (~(first | second) & MASK14))


def maximum_clique(adjacency: list[int]) -> tuple[int, list[int], int]:
    """Exact bitset branch-and-bound; returns size, one clique, call count."""
    best: list[int] = []
    calls = 0

    def expand(chosen: list[int], candidates: int) -> None:
        nonlocal best, calls
        calls += 1
        if len(chosen) + candidates.bit_count() <= len(best):
            return
        while candidates:
            if len(chosen) + candidates.bit_count() <= len(best):
                return
            bit = candidates & -candidates
            vertex = bit.bit_length() - 1
            candidates ^= bit
            expand(chosen + [vertex], candidates & adjacency[vertex])
        if len(chosen) > len(best):
            best = chosen

    expand([], (1 << len(adjacency)) - 1)
    return len(best), best, calls


def enumerate_final_profiles(masses: dict[int, Fraction]) -> dict[str, object]:
    m = 43
    minimum = min(masses.values())
    weights = [
        w for w in range(4, 16) if (m - 1) * minimum + masses[w] <= 1
    ]
    global_count = 0
    profiles: list[dict[str, int]] = []

    def visit(index: int, remaining: int, counts: list[int], mass: Fraction) -> None:
        nonlocal global_count
        cheapest = min(masses[w] for w in weights[index:])
        if mass + remaining * cheapest > 1:
            return
        if index != len(weights) - 1:
            for count in range(remaining + 1):
                visit(
                    index + 1,
                    remaining - count,
                    counts + [count],
                    mass + count * masses[weights[index]],
                )
            return
        full = counts + [remaining]
        total_mass = mass + remaining * masses[weights[index]]
        if total_mass > 1:
            return
        global_count += 1
        incidence = sum(full[i] * w for i, w in enumerate(weights))
        if incidence >= 240:
            profiles.append(
                {str(w): full[i] for i, w in enumerate(weights) if full[i]}
            )

    visit(0, m, [], Fraction(0))
    return {
        "weights_possible": weights,
        "global_chain_feasible_profile_count": global_count,
        "profiles_after_incidence_at_least_240": profiles,
    }


def main() -> None:
    witness = verify_construction(PACKAGE / "constructions/a15_42.txt")
    if not witness["valid"] or witness["parsed"] != 42:
        raise AssertionError("the 42-member lower witness failed")

    source_path = PACKAGE / "sources/a14_extremals_A303977.txt"
    families = parse_extremals(source_path)
    invalid = []
    complementary_splits = []
    profiles = Counter()
    for family_index, family in enumerate(families):
        if (
            len(family) != 28
            or any(word >= (1 << 14) for word in family)
            or not cover_free_ints(family)
        ):
            invalid.append(family_index)
            continue
        weights = tuple(sorted(Counter(word.bit_count() for word in family).items()))
        row_degrees = tuple(
            sorted(
                Counter(
                    sum(bool(word & (1 << row)) for word in family)
                    for row in range(14)
                ).items()
            )
        )
        profiles[(weights, row_degrees)] += 1
        for first in range(14):
            for second in range(first + 1, 14):
                if all(
                    bool(word & (1 << first)) != bool(word & (1 << second))
                    for word in family
                ):
                    complementary_splits.append([family_index, first, second])

    weight5_extremals = [
        family for family in families if all(word.bit_count() == 5 for word in family)
    ]
    classification_ok = (
        len(families) == 788
        and not invalid
        and not complementary_splits
        and len(weight5_extremals) == 1
        and sum(
            all(word.bit_count() == 3 for word in family) for family in families
        )
        == 787
    )
    if not classification_ok:
        raise AssertionError("the classified a(14) input failed replay")

    masses = {w: rho(15, w) for w in range(1, 16)}
    affine_slacks = {w: 546 * masses[w] - 7 - w for w in masses}
    if not all(slack >= 0 for slack in affine_slacks.values()):
        raise AssertionError("affine chain support failed")
    m44_upper = 546 - 7 * 44
    m44_lower = 15 * (44 - 28)
    if not m44_upper < m44_lower:
        raise AssertionError("44-member incidence contradiction failed")

    fixed = weight5_extremals[0]
    candidates = []
    for word in range(1 << 14):
        if word.bit_count() < 3:
            continue
        if all(
            separated(target, other, word)
            for target in fixed
            for other in fixed
            if other != target
        ):
            candidates.append(word)
    adjacency = [0] * len(candidates)
    for left_index, left in enumerate(candidates):
        for right_index in range(left_index + 1, len(candidates)):
            right = candidates[right_index]
            compatible = (
                all(separated(target, left, right) for target in fixed)
                and all(separated(left, target, right) for target in fixed)
                and all(separated(right, target, left) for target in fixed)
            )
            if compatible:
                adjacency[left_index] |= 1 << right_index
                adjacency[right_index] |= 1 << left_index
    clique_number, clique, clique_calls = maximum_clique(adjacency)
    if len(candidates) != 98 or clique_number != 14:
        raise AssertionError("degree-15 compatibility clique replay failed")

    enumeration = enumerate_final_profiles(masses)
    final_profiles = enumeration["profiles_after_incidence_at_least_240"]
    if len(final_profiles) != 7:
        raise AssertionError(f"expected seven profiles, found {len(final_profiles)}")
    delta5 = mu(15, 5, 2) - mu(15, 5, 3)
    delta7 = mu(15, 7, 3) - mu(15, 7, 4)
    eliminations = []
    for string_profile in final_profiles:
        profile = {int(w): count for w, count in string_profile.items()}
        slack = Fraction(1) - sum(
            count * masses[w] for w, count in profile.items()
        )
        q5 = floor(slack / delta5)
        q7 = floor(slack / delta7)
        b5, b7 = profile.get(5, 0), profile.get(7, 0)
        available = comb(15, 3) - (10 * b5 - q5)
        union_lower = 35 * b7 - comb(b7, 2) - 3 * comb(q7, 2)
        eliminated = union_lower > available
        eliminations.append(
            {
                "weight_profile": string_profile,
                "chain_slack": str(slack),
                "q5_max": q5,
                "q7_max": q7,
                "available_triples": available,
                "weight7_triple_union_lower": union_lower,
                "eliminated": eliminated,
            }
        )
    if not all(item["eliminated"] for item in eliminations):
        raise AssertionError("a final 43-member profile survived")

    certificate = {
        "claim": "A286874(15)=42",
        "lower_witness": witness,
        "classification": {
            "path": str(source_path.relative_to(PACKAGE)),
            "sha256": sha256(source_path),
            "parsed_families": len(families),
            "invalid_family_indices": invalid,
            "complementary_row_splits": complementary_splits,
            "all_weight3_extremals": 787,
            "all_weight5_extremals": len(weight5_extremals),
            "profile_histogram": {str(key): value for key, value in profiles.items()},
            "proves_minimum_weight_3_branch_impossible": not complementary_splits,
        },
        "m44_incidence_obstruction": {
            "affine_inequality": "w <= 546*rho(15,w)-7",
            "slack_by_weight": {str(w): str(value) for w, value in affine_slacks.items()},
            "equality_weights": [w for w, value in affine_slacks.items() if value == 0],
            "chain_incidence_upper": m44_upper,
            "row_deletion_incidence_lower": m44_lower,
            "contradiction": m44_upper < m44_lower,
        },
        "m43_degree15_obstruction": {
            "candidate_residual_words": len(candidates),
            "compatibility_edges": sum(bits.bit_count() for bits in adjacency) // 2,
            "relaxed_clique_number": clique_number,
            "required_clique_size": 15,
            "maximum_clique_words_hex": [f"{candidates[i]:04x}" for i in clique],
            "branch_calls": clique_calls,
            "proves_every_row_degree_at_least_16": clique_number < 15,
        },
        "m43_profile_enumeration": enumeration,
        "delta5_nonprivate_triple": str(delta5),
        "delta7_nonprivate_four_subset": str(delta7),
        "final_profile_eliminations": eliminations,
        "proved": witness["valid"] and all(item["eliminated"] for item in eliminations),
    }
    write_json(PACKAGE / "certificates/a15_exact.json", certificate)
    print("certified A286874(15)=42")


if __name__ == "__main__":
    main()
