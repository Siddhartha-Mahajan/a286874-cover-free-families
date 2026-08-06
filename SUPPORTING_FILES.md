# How the ancillary files support the results

## Common theorem

`scripts/common.py` implements the exact rational quantities `mu(n,w,s)` and
`rho(n,w)` from the private-subset/random-maximal-chain theorem.  It also
contains the direct cover-free verifier used for every construction and every
classified `a(14)` family.

## `A286874(15)=42`

- `constructions/a15_42.txt`, due to Steinar H. Gunderson, supplies the lower
  bound.
- `sources/a14_extremals_A303977.txt` is Steinar H. Gunderson's complete
  A303977 classification attachment.  It is used to exclude the
  minimum-weight-3 branch and identify the unique weight-5 extremal zero-cell.
- `scripts/certify_a15_exact.py` checks that classification, the affine
  incidence obstruction at 44 members, the exact degree-15 compatibility
  graph at 43 members, the remaining seven weight profiles, and their
  triple-union contradictions.
- `certificates/a15_exact.json` records every rational slack, profile and final
  comparison.

## `48 <= A286874(16) <= 54`

- `constructions/a16_48.txt`, due to Steinar H. Gunderson, supplies the lower
  bound.
- `scripts/certify_a16_upper.py` checks the `S(3,5,16)` divisibility obstruction,
  enumerates the 97 chain-feasible 55-member profiles, and tests every shared
  nonprivate-subset budget allocation against the 48-block packing bound and
  the weight-7 triple-union inequality.
- `certificates/a16_upper_54.json` contains the complete 97-profile table.

## `A286874(17)=68`

- `constructions/a17_68.txt` supplies the 68 blocks.  Siddhartha Mahajan
  produced this particular list in the audit using a CP-SAT search seeded
  with Gunderson's 52-block witness; the manuscript cites Phelps and Zhu for
  the classical `S(3,5,17)` construction literature.
- `discovery/search_constant_weight.py` is the actual CP-SAT packing-search
  program used to find the list, and `discovery/a17_seed_52.txt` is the exact
  Gunderson seed.  They document discovery but are not trusted by the proof.
- `discovery/README.md` records the two-stage search and dependency boundary.
- `scripts/certify_a17_exact.py` verifies the cover-free property, checks that
  all 680 triples occur exactly once, computes all mixed-weight chain masses
  at `n=17`, and evaluates the same universal bound for `n=18` through `22`.
- `certificates/a17_exact.json` records the `S(3,5,17)` and upper-bound checks.
  It also records `a(18)<=87`, `a(19)<=110`, `a(20)<=138`, `a(21)<=171`, and
  `a(22)<=209` as consequences of the private-chain method.

## Whole-package replay

`scripts/replay_all.py` regenerates the three claim certificates and checks
their final assertions before writing `certificates/replay_summary.json`.
`SHA256SUMS` protects the complete reproducible snapshot.
