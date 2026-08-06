# Proofs for A286874 at 15, 16 and 17

## 1. Definition

Write a binary word as the incidence vector of a subset of `[n]`.  A family
`F` is 2-cover-free when no member is contained in the union of two other
distinct members.  Equivalently, for every ordered target `C` and distinct
sources `A,B`, some row has pattern `C,A,B = 1,0,0`.

All construction files are checked directly against this definition.

## 2. Mixed-weight private-chain inequality

For a member `F`, call `S subseteq F` private to `F` when no other family
member contains `S`.  At least one of `S` and `F minus S` is private.  If not,
two other members containing the two parts would cover `F`.  Private subsets
owned by different members are cross-incomparable.

Choose a uniformly random maximal chain of the Boolean lattice by exposing a
random permutation of `[n]`.  For `|F|=w`, let `R_F` consist of the elements of
`F` appearing before the first point outside `F`.  For a fixed `S subset F`
of size `s<w`,

```text
Pr(R_F=S) = mu(n,w,s) = (n-w)/(n-s) / C(n,s),
```

while `Pr(R_F=F)=1/C(n,w)`.  The private subsets of `F` form an upset, so the
chain meets a private subset of `F` exactly when `R_F` is private.  Events
belonging to different members are disjoint.

Pair each subset of `F` with its complement in `F`.  The larger side has the
smaller `mu` mass.  Thus, writing `w=2t-1` or `w=2t`, define

```text
rho(n,2t-1) = sum_{s=t}^{2t-1} C(2t-1,s) mu(n,2t-1,s),

rho(n,2t)   = (1/2) C(2t,t) mu(n,2t,t)
               + sum_{s=t+1}^{2t} C(2t,s) mu(n,2t,s).
```

Every family of at least three members therefore satisfies

```text
sum_{F in family} rho(n,|F|) <= 1.                 (1)
```

`scripts/common.py` evaluates `mu` and `rho` with exact rational arithmetic.

## 3. Exact value `a(17)=68`

At `n=17`, the minimum of `rho(17,w)` over all weights is `1/68`, attained
only at weights 5 and 7.  Equation (1) gives `|F|<=68` for arbitrary mixed
weights.

`constructions/a17_68.txt` contains 68 weight-5 members.  Every pair meets in
at most two points, so no member can be covered by two others.  Moreover,

```text
68*C(5,3) = C(17,3),
```

and the replay checks that all 680 block triples are distinct.  Hence the
construction is an `S(3,5,17)` and

```text
a(17)=68.
```

The exact arithmetic and witness verification are in
`certificates/a17_exact.json`.

## 4. Exact value `a(15)=42`

### 4.1 Lower bound

The 42 words in `constructions/a15_42.txt` pass the complete cover-free test.

### 4.2 Excluding 44 members

For every weight `1<=w<=15`, direct rational evaluation gives

```text
w <= 546*rho(15,w)-7,                              (2)
```

with equality only at weights 5 and 7.  If `I=sum_F |F|` and the family has
`m` members, equations (1) and (2) give

```text
I <= 546-7m.                                       (3)
```

Fix a row and keep the members zero on that row.  After deleting the row this
is a cover-free family on 14 rows, so it has at most `a(14)=28` members.  Every
row in an `m`-member family therefore has degree at least `m-28`, giving

```text
I >= 15(m-28).                                     (4)
```

At `m=44`, (3) gives `I<=238` while (4) gives `I>=240`.  Thus `a(15)<=43`.

### 4.3 Excluding minimum weight 3 at 43 members

Suppose a minimum member `C` has size 3.  For each of the other 42 members,
take its nonempty zero trace on `C`.  These traces are pairwise intersecting;
otherwise two members cover `C`.  Each point of `C` occurs in at most 28
traces by the `a(14)=28` row-cell bound.

A singleton trace would force all 42 traces through one point, impossible.
Hence all traces have size at least 2.  Their total incidence is at least
`42*2=84` and at most `3*28=84`.  Equality forces fourteen copies of each of
the three 2-subsets of `C`.

The union of any two 14-member trace classes has a constant-zero support row.
Deleting it gives an extremal 28-member family on 14 rows whose two remaining
support rows are complementary.  The file
`sources/a14_extremals_A303977.txt` is the complete 788-family classification.
The replay verifies every family directly and finds no complementary row pair.
Therefore minimum weight 3 is impossible.

### 4.4 Excluding a degree-15 row

Now every member has weight at least 4.  Equation (4) says every row has
degree at least 15.  If one row had degree 15, its 28-member zero-cell would be
an extremal family on 14 rows.  The verified classification consists of 787
all-weight-3 families and one all-weight-5 family.  Minimum weight at least 4
forces the unique weight-5 extremal.

Fix this extremal as the zero-cell.  Exhaust all `2^14` residual words for a
one-cell member, requiring residual weight at least 3 and every cover-free
condition involving one candidate and two fixed members.  Exactly 98
candidates remain.  Join two candidates when every condition involving the
fixed family and those two candidates holds.  This deliberately omits covers
among three selected one-cell members, so it is a relaxation.

The exact bitset branch-and-bound replay finds that this 98-vertex graph has
clique number 14.  Fifteen one-cell members would require a 15-clique.
Therefore degree 15 is impossible, every row has degree at least 16, and

```text
I >= 15*16 = 240.                                  (5)
```

### 4.5 The seven remaining profiles

Enumerating all integer weight profiles satisfying (1), minimum weight at
least 4, 43 total members and (5) leaves exactly

```text
5^28 7^15
5^29 7^14
5^29 6^1 7^13
5^29 6^2 7^12
5^30 7^13
5^30 6^1 7^12
5^31 7^11 8^1.
```

A nonprivate triple of a weight-5 member reverses one complementary choice in
the chain calculation and costs

```text
mu(15,5,2)-mu(15,5,3) = 1/182.
```

Similarly a nonprivate 4-subset of a weight-7 member costs

```text
mu(15,7,3)-mu(15,7,4) = 2/2145.
```

Let the profile slack allow at most `q5` and `q7` such incidences.  At least
`10*b5-q5` triples are private to the `b5` weight-5 members, and consequently
occur in no weight-7 member.

For the `b7` weight-7 members, let `r_Q` count members containing a fixed
4-set `Q`.  If `r_Q>=2`, all `r_Q` incidences are nonprivate, so

```text
sum_Q C(r_Q,2) <= C(q7,2).
```

For `0<=r<=7`, `C(r,3)<=1+3C(r,4)`.  Two-term inclusion-exclusion therefore
gives the following lower bound for the union of triples in the weight-7
members:

```text
35*b7 - C(b7,2) - 3*C(q7,2).                       (6)
```

For the seven profiles, (6) gives respectively

```text
420, 390, 377, 354, 314, 324, 330,
```

while only

```text
175, 165, 165, 165, 156, 156, 145
```

triples are available outside the private weight-5 triples.  All seven cases
are impossible.  Combined with the 42-member witness,

```text
a(15)=42.
```

The complete replay record is `certificates/a15_exact.json`.

## 5. New upper bound `a(16)<=54`

The witness `constructions/a16_48.txt` proves `a(16)>=48`.

At `n=16`, the unique minimum chain mass is `rho(16,5)=1/56`.  Equality with
56 members would make all members weight 5 with all triples private.  Their
560 triples would form an `S(3,5,16)`, but its point replication number would
be

```text
C(15,2)/C(4,2) = 35/2,
```

which is not integral.  Thus `a(16)<=55`.

To exclude 55, exact enumeration of (1) leaves 97 integer weight profiles,
supported on weights 3 through 9.  Two necessary conditions eliminate them.

First, weight-5 members with all triples private form a `3-(16,5,<=1)`
packing.  Through a point there are at most

```text
floor(15/4 * floor(14/3)) = 15
```

blocks, and hence the packing has at most `16*15/5=48` blocks.  If `q5`
weight-5 triple incidences are nonprivate, deleting at most `q5` affected
members leaves such a packing, so necessarily

```text
b5-q5 <= 48.                                       (7)
```

The exact chain cost is

```text
delta5 = mu(16,5,2)-mu(16,5,3) = 11/2184.
```

Second, for weight-7 members the same triple-union argument (6) applies, with

```text
delta7 = mu(16,7,3)-mu(16,7,4) = 3/3640.
```

Their triple union must fit among the

```text
C(16,3)-(10*b5-q5)
```

triples not private to weight-5 members.  Crucially, `q5` and `q7` spend one
shared profile slack:

```text
q5*(11/2184) + q7*(3/3640) <= slack.               (8)
```

`scripts/certify_a16_upper.py` enumerates every integer `(q5,q7)` satisfying
(8) for every one of the 97 profiles and checks (6) and (7).  No allocation
survives.  Therefore no 55-member family exists, and

```text
48 <= a(16) <= 54.
```

The machine-readable table of all 97 eliminations is
`certificates/a16_upper_54.json`.  No exact value at `n=16` is claimed.
