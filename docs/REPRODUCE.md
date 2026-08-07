# Reproducing the certificates

## Requirements

- Python 3.10 or newer.
- No third-party packages.

All commands below are run from the package root.

## Full replay

```sh
python3 scripts/replay_all.py
```

This regenerates:

- `certificates/chain_formula.json`;
- `certificates/a15_exact.json`;
- `certificates/a16_upper_54.json`;
- `certificates/a17_exact.json`;
- `certificates/replay_summary.json`.

## Individual claims

```sh
python3 scripts/certify_chain_formula.py
python3 scripts/certify_a15_exact.py
python3 scripts/certify_a16_upper.py
python3 scripts/certify_a17_exact.py
```

The chain-formula replay compares the defining rational sums with both closed
forms at every weight for `3<=n<=250`, checks the minimizing-weight rule, and
checks the resulting integral bound.  The all-`n` statement itself is proved
symbolically in the manuscript.  The `a(15)` replay checks all 788 classified
extremal `a(14)` families, the 44-member incidence contradiction, the exact
98-vertex degree-15 gluing graph,
and the final seven profiles.  The `a(16)` replay enumerates and eliminates all
97 chain-feasible 55-member profiles.  The `a(17)` replay verifies both the
68-word construction and all 17 exact chain masses.

## Integrity check

On macOS:

```sh
shasum -a 256 -c SHA256SUMS
```

On systems with GNU coreutils:

```sh
sha256sum -c SHA256SUMS
```

To rebuild the checksum list after intentionally changing or regenerating a
file:

```sh
python3 scripts/build_sha256s.py
```

The JSON output is deterministic and contains no timestamps or absolute paths.

## Optional historical discovery search

The proof replay above does not require OR-Tools.  The actual CP-SAT program
used to discover the particular labeled `n=17` construction and its exact
52-vector seed are retained under `discovery/`; see
`discovery/README.md`.  Parallel CP-SAT search is heuristic and is not relied
upon for independent verification of the saved construction.
