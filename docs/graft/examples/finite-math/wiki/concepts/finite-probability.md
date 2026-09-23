---
title: Finite probability
sources:
  - raw/finite-probability.md
compiled: 2026-09-23
---

# Finite probability

A **finite sample space** S is the set of all possible outcomes of an
experiment. An **event** E is a subset of S. When all outcomes are
equally likely, P(E) = |E| / |S| — so probability reduces to the
counting described in [sets and counting](sets-and-counting.md).

On a finite space the axioms are: 0 ≤ P(E) ≤ 1, P(S) = 1, and for
disjoint events P(E ∪ F) = P(E) + P(F). In general,
P(E ∪ F) = P(E) + P(F) − P(E ∩ F).

**Conditional probability** is P(E | F) = P(E ∩ F) / P(F) when
P(F) > 0. Events E and F are **independent** when
P(E ∩ F) = P(E)·P(F).

**Bayes' theorem** (two-event form):
P(F | E) = P(E | F)·P(F) / P(E).

The **expected value** of a random variable X taking values
x1, …, xn with probabilities p1, …, pn is
E(X) = x1·p1 + … + xn·pn.

Example: rolling two fair dice gives |S| = 36; the event "sum is 7"
has 6 outcomes, so its probability is 6/36 = 1/6.
