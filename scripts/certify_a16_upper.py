#!/usr/bin/env python3
"""Certify the new unrestricted upper bound A286874(16)<=54."""

from __future__ import annotations

from fractions import Fraction
from math import comb, floor

from common import PACKAGE, mu, rho, verify_construction, write_json


def enumerate_profiles(masses: dict[int, Fraction], m: int) -> list[dict[str, int]]:
    minimum = min(masses.values())
    weights = [w for w in masses if (m - 1) * minimum + masses[w] <= 1]
    profiles: list[dict[str, int]] = []

    def visit(index: int, remaining: int, counts: list[int], mass: Fraction) -> None:
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
        if mass + remaining * masses[weights[index]] <= 1:
            profiles.append(
                {str(w): full[i] for i, w in enumerate(weights) if full[i]}
            )

    visit(0, m, [], Fraction(0))
    return profiles


def main() -> None:
    lower_witness = verify_construction(PACKAGE / "constructions/a16_48.txt")
    if not lower_witness["valid"] or lower_witness["parsed"] != 48:
        raise AssertionError("the 48-member lower witness failed")

    masses = {w: rho(16, w) for w in range(1, 17)}
    minimum = min(masses.values())
    minimizing_weights = [w for w, value in masses.items() if value == minimum]
    replication = Fraction(comb(15, 2), comb(4, 2))
    if minimum != Fraction(1, 56) or minimizing_weights != [5]:
        raise AssertionError("unexpected n=16 chain minimum")
    if replication.denominator == 1:
        raise AssertionError("S(3,5,16) divisibility obstruction disappeared")

    profiles = enumerate_profiles(masses, 55)
    if len(profiles) != 97:
        raise AssertionError(f"expected 97 profiles, found {len(profiles)}")
    delta5 = mu(16, 5, 2) - mu(16, 5, 3)
    delta7 = mu(16, 7, 3) - mu(16, 7, 4)
    if delta5 != Fraction(11, 2184) or delta7 != Fraction(3, 3640):
        raise AssertionError("unexpected n=16 nonprivate-subset costs")

    records = []
    survivors = []
    for string_profile in profiles:
        profile = {int(w): count for w, count in string_profile.items()}
        slack = Fraction(1) - sum(
            count * masses[w] for w, count in profile.items()
        )
        b5, b7 = profile.get(5, 0), profile.get(7, 0)
        feasible_allocations = []
        for q5 in range(floor(slack / delta5) + 1):
            remaining = slack - q5 * delta5
            for q7 in range(floor(remaining / delta7) + 1):
                packing_ok = b5 - q5 <= 48
                available = comb(16, 3) - (10 * b5 - q5)
                union_lower = 35 * b7 - comb(b7, 2) - 3 * comb(q7, 2)
                if packing_ok and union_lower <= available:
                    feasible_allocations.append({"q5": q5, "q7": q7})
        if feasible_allocations:
            survivors.append(string_profile)
        records.append(
            {
                "weight_profile": string_profile,
                "chain_slack": str(slack),
                "q5_max_if_all_slack_used_there": floor(slack / delta5),
                "q7_max_if_all_slack_used_there": floor(slack / delta7),
                "jointly_feasible_allocations": feasible_allocations,
                "eliminated": not feasible_allocations,
            }
        )
    if survivors:
        raise AssertionError(f"55-member profiles survived: {survivors}")

    certificate = {
        "claim": "48 <= A286874(16) <= 54",
        "lower_witness": lower_witness,
        "rho_by_weight": {str(w): str(value) for w, value in masses.items()},
        "raw_chain_upper": 56,
        "unique_chain_minimizing_weight": minimizing_weights,
        "S_3_5_16_point_replication": str(replication),
        "proves_no_56_member_family": replication.denominator != 1,
        "m55_chain_feasible_profile_count": len(profiles),
        "delta5_nonprivate_triple": str(delta5),
        "delta7_nonprivate_four_subset": str(delta7),
        "weight5_triple_packing_upper": 48,
        "m55_profile_records": records,
        "m55_surviving_profiles": survivors,
        "proves_no_55_member_family": not survivors,
        "proved": lower_witness["valid"] and not survivors,
    }
    write_json(PACKAGE / "certificates/a16_upper_54.json", certificate)
    print("certified 48 <= A286874(16) <= 54")


if __name__ == "__main__":
    main()
