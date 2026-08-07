#!/usr/bin/env python3
"""Audit the closed private-chain formulas and all-dimensions bound."""

from __future__ import annotations

from fractions import Fraction
from math import comb, floor

from common import PACKAGE, rho, write_json


def closed_rho(n: int, w: int) -> Fraction:
    """Closed form for rho(n,w), split by the parity of w."""
    if w % 2:
        t = (w + 1) // 2
        return Fraction(comb(2 * t - 1, t), comb(n, t))
    t = w // 2
    return Fraction(n, 2 * t) * Fraction(
        comb(n - t - 1, t - 1), comb(n, 2 * t)
    )


def main() -> None:
    rows = []
    for n in range(3, 251):
        defining_masses = {w: rho(n, w) for w in range(1, n + 1)}
        closed_masses = {w: closed_rho(n, w) for w in range(1, n + 1)}
        if defining_masses != closed_masses:
            raise AssertionError(f"closed rho formula failed at n={n}")

        minimum = min(defining_masses.values())
        minimum_weights = [
            w for w, value in defining_masses.items() if value == minimum
        ]
        t = (n + 2) // 5  # ceiling((n-2)/5)
        predicted_weights = [2 * t - 1]
        if n % 5 == 2:
            predicted_weights.append(2 * t + 1)
        if minimum_weights != predicted_weights:
            raise AssertionError(
                f"minimizing weights failed at n={n}: "
                f"{minimum_weights} != {predicted_weights}"
            )

        chain_bound = floor(Fraction(1, 1) / minimum)
        formula_bound = floor(Fraction(comb(n, t), comb(2 * t - 1, t)))
        if chain_bound != formula_bound:
            raise AssertionError(f"integral bound formula failed at n={n}")

        rows.append(
            {
                "n": n,
                "t": t,
                "minimum_rho": str(minimum),
                "minimum_weights": minimum_weights,
                "chain_upper_bound": chain_bound,
            }
        )

    certificate = {
        "claim": (
            "For n>=3 and t=ceiling((n-2)/5), "
            "A286874(n)<=floor(C(n,t)/C(2t-1,t))"
        ),
        "closed_forms": {
            "odd_weight_2t_minus_1": "C(2t-1,t)/C(n,t)",
            "even_weight_2t": "n*C(n-t-1,t-1)/(2t*C(n,2t))",
        },
        "symbolic_proof_location": "manuscript/a286874_bounds.tex",
        "implementation_checked_range": [3, 250],
        "rows": rows,
        "proved": True,
    }
    write_json(PACKAGE / "certificates/chain_formula.json", certificate)
    print("certified the closed private-chain formula through n=250")


if __name__ == "__main__":
    main()
