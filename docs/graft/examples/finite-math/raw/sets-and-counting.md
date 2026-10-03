# Notes: sets and counting

A set is an unordered collection of distinct objects, called elements.
A set A is a subset of B when every element of A is also in B. A finite
set with n elements has 2^n subsets.

Basic operations: union (A ∪ B), intersection (A ∩ B), complement (A′
relative to a universal set U). Inclusion–exclusion for two sets:
|A ∪ B| = |A| + |B| − |A ∩ B|.

Counting principles:

- Multiplication principle: a task done in k stages with n1, n2, …, nk
  choices per stage can be done in n1·n2·…·nk ways.
- Permutations: ordered arrangements of r objects chosen from n distinct
  objects: P(n, r) = n! / (n − r)!.
- Combinations: unordered selections of r objects from n:
  C(n, r) = n! / (r!(n − r)!).

Worked example: choosing a 3-person committee from 10 people is
C(10, 3) = 120; electing a president, secretary, and treasurer from the
same 10 people is P(10, 3) = 720.
