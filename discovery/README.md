# Historical `n=17` discovery search

This directory contains the search program used to find the packaged
68-block construction and the 52-block OEIS witness used as its initial hint.

- `search_constant_weight.py` is the search program used in the audit.
- `a17_seed_52.txt` is Steinar H. Gunderson's 52-vector construction from the
  OEIS A286874 attachment `a286874_3.txt`.

The search proceeded in two stages: the 52-block witness was used to find a
55-block improvement, and that improvement was then used as the hint for the
run that found 68 blocks.  The intermediate 55-block output was overwritten
during the original search and is not a mathematical input to any final
claim.  CP-SAT reported objective and bound 68 for the successful run.

The program requires OR-Tools and parallel CP-SAT search is not intended to
reproduce the same labeled solution deterministically.  A representative
invocation is:

```sh
python3 discovery/search_constant_weight.py 17 \
  --weight 5 --intersection 2 --seconds 300 --workers 8 --seed 1 \
  --hint discovery/a17_seed_52.txt \
  --output discovery/a17_search_output.txt
```

Neither OR-Tools nor successful repetition of the search is required for the
proof.  `scripts/certify_a17_exact.py` independently verifies the saved
68-vector output, its complete Steiner triple incidence, and the matching
mixed-weight upper bound using only Python's standard library.
