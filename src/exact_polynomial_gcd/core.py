"""Core implementation of exact polynomial GCD."""

from fractions import Fraction
from typing import List, Tuple, Union


def _trim(coefficients: List[Fraction]) -> List[Fraction]:
    """Remove trailing zero coefficients without mutating the input.

    A polynomial is represented as a list of coefficients in increasing
    degree order.  Trailing zeros do not change the polynomial, so they
    are removed for canonical output.
    """
    result = list(coefficients)
    while result and result[-1] == 0:
        result.pop()
    return result


def _normalize(coefficients: List[Fraction]) -> List[Fraction]:
    """Make a polynomial's leading coefficient 1.

    The GCD is unique only up to multiplication by a non-zero rational,
    so we choose the monic representative.  If the polynomial is zero,
    the empty list is returned.
    """
    trimmed = _trim(coefficients)
    if not trimmed:
        return []
    leading = trimmed[-1]
    if leading == 1:
        return trimmed
    return [coeff / leading for coeff in trimmed]


def _degree(coefficients: List[Fraction]) -> int:
    """Return the degree of the polynomial, or -1 for the zero polynomial."""
    trimmed = _trim(coefficients)
    return len(trimmed) - 1


def _poly_divmod(
    numerator: List[Fraction], denominator: List[Fraction]
) -> Tuple[List[Fraction], List[Fraction]]:
    """Divide one polynomial by another, returning (quotient, remainder).

    Both polynomials are given in increasing degree order.  The denominator
    must be non-zero.  Division uses exact Fraction arithmetic, so no
    rounding or approximation occurs.
    """
    numerator = _trim(numerator)
    denominator = _trim(denominator)
    if not denominator:
        raise ZeroDivisionError("polynomial division by zero")

    denom_degree = _degree(denominator)
    denom_lead = denominator[-1]

    remainder = list(numerator)
    quotient_degree = max(-1, _degree(remainder) - denom_degree)
    quotient = [Fraction(0)] * (quotient_degree + 1)

    while _degree(remainder) >= denom_degree:
        remainder_degree = _degree(remainder)
        shift = remainder_degree - denom_degree
        factor = remainder[remainder_degree] / denom_lead
        quotient[shift] = factor

        # Subtract factor * x^shift * denominator from remainder.
        for i in range(denom_degree + 1):
            remainder[shift + i] -= factor * denominator[i]

        remainder = _trim(remainder)

    return _trim(quotient), remainder


def polynomial_gcd(
    a: List[Union[Fraction, int]], b: List[Union[Fraction, int]]
) -> List[Fraction]:
    """Compute the monic greatest common divisor of two polynomials.

    The polynomials ``a`` and ``b`` are represented as lists of
    coefficients in increasing degree order.  Coefficients may be
    ``Fraction`` instances or integers; they are converted to
    ``Fraction`` internally.

    The Euclidean algorithm over ``Fraction`` is used.  Because all
    arithmetic is exact, the result is guaranteed to be a common divisor
    whose leading coefficient is 1.  If both inputs are the zero
    polynomial, the result is the zero polynomial (empty list).

    Args:
        a: Coefficients of the first polynomial.
        b: Coefficients of the second polynomial.

    Returns:
        A list of ``Fraction`` coefficients in increasing degree order
        representing the monic GCD.
    """
    a = _trim([Fraction(coeff) for coeff in a])
    b = _trim([Fraction(coeff) for coeff in b])

    while b:
        _, remainder = _poly_divmod(a, b)
        a, b = b, remainder

    # The zero polynomial case: gcd(0, 0) should remain empty.
    if not a:
        return []

    # For any non-zero polynomial, gcd(p, 0) is the monic version of p.
    return _normalize(a)
