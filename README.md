# Exact Polynomial GCD

Computes the greatest common divisor of two univariate polynomials with rational coefficients using the Euclidean algorithm over `Fraction`.

## Usage

```python
from fractions import Fraction
from exact_polynomial_gcd import polynomial_gcd

# x^2 - 1 = (x - 1)(x + 1)
a = [-1, 0, 1]
# x^3 - x = x(x - 1)(x + 1)
b = [0, -1, 0, 1]

print(polynomial_gcd(a, b))
# [1, 0, -1]  (monic x^2 - 1)
```

Coefficients may be `Fraction` or `int`. The result is always a list of `Fraction` in increasing degree order, with the leading coefficient normalized to 1. The zero polynomial is represented as an empty list.

## Why this library exists

Finding polynomial GCDs is a building block for simplifying rational functions and solving polynomial systems. Floating-point implementations suffer from rounding error that can make near-common factors disappear or introduce spurious ones. This library uses exact rational arithmetic (`fractions.Fraction`) so the answer is always mathematically exact, at the cost of speed for large or high-degree inputs.

The main awkward edge is the zero polynomial: `gcd(0, 0)` is defined as `0` here, not `1`. This matches the convention that the zero polynomial is its own greatest divisor. For any non-zero polynomial, the GCD with zero is the monic version of that polynomial.

## Exported names

- `polynomial_gcd(a, b)` — compute the monic GCD of two polynomials given as coefficient lists in increasing degree order.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

