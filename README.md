# Exact values and an all-dimensions upper bound for A286874

Reproducible research package by **Siddhartha Mahajan and Paras Chopra** for the binary
2-cover-free-family sequence [OEIS A286874](https://oeis.org/A286874).

The package establishes

```text
A286874(15) = 42,
48 <= A286874(16) <= 54,
A286874(17) = 68.
```

It also proves the explicit universal bound

```text
For n>=3 and t=ceiling((n-2)/5),
A286874(n) <= floor(C(n,t)/C(2t-1,t)).
```

The `n=15` and `n=17` statements are exact evaluations.  The `n=16`
statement improves the unrestricted upper bound; no exact value at `n=16` is
claimed.  The all-dimensions formula gives, in particular,
`a(18)<=87`, `a(19)<=110`, `a(20)<=138`, `a(21)<=171`, and `a(22)<=209`;
these are stated as consequences of this method, not as a claim about the
best bounds from all sources.

## Independent verification

Only Python's standard library is required:

```sh
python3 scripts/replay_all.py
```

Expected output:

```text
certified the closed private-chain formula through n=250
certified A286874(15)=42
certified 48 <= A286874(16) <= 54
certified A286874(17)=68
all final A286874 certificates passed
```

The replay compares the defining chain sums with the closed formula at every
weight through `n=250`, verifies all construction vectors against the original
bitwise-OR definition, checks every one of the 788 classified extremal
`a(14)` families,
reconstructs the 98-vertex compatibility graph used at `n=15`, exhausts the
seven final `n=15` profiles, and eliminates all 97 chain-feasible
55-member profiles at `n=16`.  All arithmetic is exact.

## Repository contents

- [manuscript/a286874_bounds.pdf](manuscript/a286874_bounds.pdf): paper-style
  statement and proof.
- [docs/PROOF.md](docs/PROOF.md): expanded readable proof.
- [docs/REPRODUCE.md](docs/REPRODUCE.md): replay instructions.
- [SUPPORTING_FILES.md](SUPPORTING_FILES.md): how the ancillary files support
  each mathematical claim.
- `scripts/`: final standard-library certifiers.
- `discovery/`: the historical CP-SAT search program and Gunderson's 52-vector
  seed used to find the particular `n=17` witness; these are not proof inputs.
- `constructions/`: the 42-, 48-, and 68-member witnesses.
- `sources/`: the indispensable complete A303977 classification input.
- `certificates/`: deterministic JSON replay records.
- `SHA256SUMS`: integrity hashes for the repository snapshot.

## Build commands

```sh
make verify       # replay all mathematical certificates
make paper        # compile the manuscript with Tectonic
make checksums    # regenerate SHA256SUMS
```

The precise mathematical role of the private-chain inequality and each finite
certificate is explained in the manuscript; the computations are reductions
of explicitly stated lemmas, not evidence from solver timeouts.

## Authors

Siddhartha Mahajan and Paras Chopra, 2026.

## Construction and data credits

- Steinar H. Gunderson supplied the packaged 42-vector construction at
  `n=15`, the packaged 48-vector construction at `n=16`, and the complete
  788-class `n=14` attachment used in the upper-bound proof.
- The particular 68-vector `S(3,5,17)` list was produced by Siddhartha Mahajan
  during this audit using a CP-SAT search seeded with Gunderson's earlier
  52-vector construction.  Its validity and Steiner property are replayed
  without trusting that search.
- K. T. Phelps and L. Zhu are cited in the manuscript for the classical
  inversive-plane and explicit `S(3,5,17)` construction literature.
- OEIS A303977 was created by Zhao Hui Du; its complete `n=14` attachment and
  `a(14)` extension were contributed by Gunderson.  Dmitry Kamenetsky is cited
  for the earlier 28-vector lower-bound construction at `n=14`.

See [CITATION.cff](CITATION.cff) for citation metadata and [LICENSE.md](LICENSE.md)
for reuse terms.
