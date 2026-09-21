"""Exact polynomial GCD over rational coefficients.

This package provides one function, :func:`polynomial_gcd`, that computes
the greatest common divisor of two univariate polynomials whose
coefficients are exact rational numbers (``fractions.Fraction``).
"""

from .core import polynomial_gcd

__all__ = ["polynomial_gcd"]
