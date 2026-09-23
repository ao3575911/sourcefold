---
title: Matrices and linear systems
sources:
  - raw/matrices-linear-systems.md
compiled: 2026-09-23
---

# Matrices and linear systems

A **matrix** is a rectangular array of numbers with m rows and n
columns. Matrices of the same size are added entrywise, and a scalar
multiplies every entry. The product AB is defined when the column
count of A equals the row count of B; entry (i, j) of AB is the dot
product of row i of A with column j of B. Matrix multiplication is
not commutative in general.

The **identity matrix** I has ones on the diagonal and zeros
elsewhere, and satisfies AI = IA = A. A square matrix A is
**invertible** when there is a matrix A⁻¹ with AA⁻¹ = A⁻¹A = I.

## Solving linear systems

A system of linear equations can be written as the matrix equation
AX = B. **Gauss–Jordan elimination** row-reduces the augmented matrix
[A | B] to reduced row echelon form using three row operations:

1. swap two rows;
2. multiply a row by a nonzero constant;
3. add a multiple of one row to another.

Every system has exactly one of: a unique solution, infinitely many
solutions, or no solution. For a 2×2 matrix [[a, b], [c, d]], the
**determinant** is ad − bc, and the matrix is invertible exactly when
the determinant is nonzero.
