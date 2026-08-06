# Source provenance

## Complete `a(14)` extremal classification

`a14_extremals_A303977.txt` is copied byte-for-byte from the audit source

```text
../../sprints/sprint_01_exact_values/sources/a303977_all_a14_extremals.txt
```

It is Steinar H. Gunderson's OEIS A303977 attachment containing all 788
equivalence classes of 28-member extremal families on 14 points.  A303977 was
created by Zhao Hui Du; Gunderson contributed the `a(14)` classification and
attached file on February 18, 2026.  The final replay does not trust the format
semantically: it parses all 788 families, checks size, bit range, distinctness
and the complete 2-cover-free condition, then checks the exact row and weight
facts used in the proof.  Dmitry Kamenetsky's earlier A286874 attachment
contains the historical 28-vector lower-bound construction at `n=14`; it is
cited in the manuscript, although the final replay uses Gunderson's complete
classification file rather than Kamenetsky's separate witness.

SHA-256:

```text
22c962481d737737ab1f25c88e7cfec1f24c9f5e4bb5caee8450956bd80b79c4
```

## Construction witnesses

The `n=15` and `n=16` witnesses are extracted unchanged from Steinar H.
Gunderson's captured A286874 attachment `../../sources/a286874_3.txt`.  The
packaged `n=17` witness is the verified 68-block `S(3,5,17)` retained in
`../../outputs/n17_weight5_at_least_56.txt`; Siddhartha Mahajan produced that
particular list during this audit by a CP-SAT packing search seeded with
Gunderson's 52-block construction.  Phelps (1981) and Zhu (1980), cited in the
manuscript, supply the classical design references.  Each packaged witness is
checked directly against the original OR-containment definition.

```text
eeaaca0d7e5f63c402fbd42ae5ab3583340e4633022a689f3b499681b7ada371  constructions/a15_42.txt
3e91ef56158a572d7e4793deb8f7a4cb2acd38e6c32f62d0b5cda981e146060b  constructions/a16_48.txt
d7bf1d38e429f600b8bee5edd7dd082e732b5516a08afc045a7cfabccc2ca9c3  constructions/a17_68.txt
```
