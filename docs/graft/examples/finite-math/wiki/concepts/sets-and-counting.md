---
title: Sets and counting
sources:
  - raw/sets-and-counting.md
compiled: 2026-09-23
---

# Sets and counting

A **set** is an unordered collection of distinct objects, called
elements. A set A is a **subset** of B when every element of A is also
an element of B. A finite set with n elements has 2^n subsets.

The basic operations are union (A ∪ B), intersection (A ∩ B), and
complement (A′ relative to a universal set U). For two finite sets,
inclusion–exclusion gives |A ∪ B| = |A| + |B| − |A ∩ B|.

## Counting principles

- **Multiplication principle.** A task done in k stages with
  n1, n2, …, nk choices per stage can be done in n1·n2·…·nk ways.
- **Permutations** are ordered arrangements of r objects chosen from n
  distinct objects: P(n, r) = n! / (n − r)!.
- **Combinations** are unordered selections of r objects from n:
  C(n, r) = n! / (r!(n − r)!).

Example: choosing a 3-person committee from 10 people is
C(10, 3) = 120, while electing a president, secretary, and treasurer
from the same 10 people is P(10, 3) = 720.

Counting subsets of a sample space is the basis of
[finite probability](finite-probability.md).
