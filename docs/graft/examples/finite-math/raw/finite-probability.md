# Notes: probability on finite sample spaces

A finite sample space S is the set of all possible outcomes of an
experiment. An event E is a subset of S. When all outcomes are equally
likely, P(E) = |E| / |S|.

Axioms on a finite space: 0 ≤ P(E) ≤ 1, P(S) = 1, and for disjoint
events P(E ∪ F) = P(E) + P(F). In general,
P(E ∪ F) = P(E) + P(F) − P(E ∩ F).

Conditional probability: P(E | F) = P(E ∩ F) / P(F) when P(F) > 0.
Events E and F are independent when P(E ∩ F) = P(E)·P(F).

Bayes' theorem (two-event form):
P(F | E) = P(E | F)·P(F) / P(E).

Expected value of a random variable X taking values x1, …, xn with
probabilities p1, …, pn: E(X) = x1·p1 + … + xn·pn.

Worked example: rolling two fair dice, |S| = 36; the event "sum is 7"
has 6 outcomes, so its probability is 6/36 = 1/6.
