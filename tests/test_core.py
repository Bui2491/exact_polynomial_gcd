import unittest
from fractions import Fraction

from exact_polynomial_gcd import polynomial_gcd


class PolynomialGCDTests(unittest.TestCase):
    def assertPolyEqual(self, actual, expected):
        self.assertEqual(actual, expected)

    def test_zero_and_zero(self):
        self.assertPolyEqual(polynomial_gcd([], []), [])

    def test_zero_and_nonzero(self):
        self.assertPolyEqual(polynomial_gcd([], [1, 2]), [Fraction(1, 2), 1])

    def test_nonzero_and_zero(self):
        self.assertPolyEqual(polynomial_gcd([3, 0, 1], []), [3, 0, 1])

    def test_coprime_linear(self):
        self.assertPolyEqual(polynomial_gcd([1, 1], [2, 1]), [1])

    def test_common_linear_factor(self):
        # (x+1) and (x+2)(x+1) = x^2+3x+2
        self.assertPolyEqual(polynomial_gcd([1, 1], [2, 3, 1]), [1, 1])

    def test_common_quadratic_factor(self):
        # a = (x^2+1)(x+1) = x^3+x^2+x+1
        # b = (x^2+1)(x-1) = x^3-x^2+x-1
        a = [1, 1, 1, 1]
        b = [-1, 1, -1, 1]
        self.assertPolyEqual(polynomial_gcd(a, b), [1, 0, 1])

    def test_integer_coefficients_are_accepted(self):
        self.assertPolyEqual(polynomial_gcd([1, 1], [1, 1]), [1, 1])

    def test_fraction_coefficients(self):
        a = [Fraction(1, 2), Fraction(1, 2)]
        b = [1, 1]
        self.assertPolyEqual(polynomial_gcd(a, b), [1, 1])

    def test_non_monic_result_is_normalized(self):
        # a = 2x+2, b = 3x+3 -> gcd is x+1, not 6x+6
        self.assertPolyEqual(polynomial_gcd([2, 2], [3, 3]), [1, 1])

    def test_constant_gcd(self):
        # a = 4x+6, b = 4x+2 -> gcd is 2, normalized to 1
        self.assertPolyEqual(polynomial_gcd([6, 4], [2, 4]), [1])

    def test_identical_polynomials(self):
        a = [1, 2, 3]
        self.assertPolyEqual(polynomial_gcd(a, a), [Fraction(1, 3), Fraction(2, 3), 1])

    def test_trailing_zeros_are_ignored(self):
        a = [1, 1, 0, 0]
        b = [1, 1]
        self.assertPolyEqual(polynomial_gcd(a, b), [1, 1])

    def test_one_polynomial_divides_other(self):
        a = [1, 0, 1]  # x^2+1
        b = [1, 0, 2, 0, 1]  # x^4+2x^2+1 = (x^2+1)^2
        self.assertPolyEqual(polynomial_gcd(a, b), [1, 0, 1])

    def test_large_degree_difference(self):
        # a = x^5, b = x^2
        a = [0, 0, 0, 0, 0, 1]
        b = [0, 0, 1]
        self.assertPolyEqual(polynomial_gcd(a, b), [0, 0, 1])

    def test_negative_coefficients(self):
        a = [1, -2, 1]  # x^2-2x+1 = (x-1)^2
        b = [1, -1]  # x-1
        self.assertPolyEqual(polynomial_gcd(a, b), [-1, 1])


if __name__ == "__main__":
    unittest.main()
