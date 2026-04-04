from fraction import Fraction
from matrix import *


def test_first_step():
    original_matrix = [
        [Fraction(3), Fraction(2), Fraction(5), Fraction(4), Fraction(3)],
        [Fraction(1), Fraction(-1), Fraction(-1), Fraction(-4), Fraction(-2)],
        [Fraction(4), Fraction(1), Fraction(4), Fraction(0), Fraction(2)],
    ]

    a = copy_matrix(original_matrix)

    row = 0
    col = find_enabling_element(a, row)
    a_hat = transform_matrix(a, row, col)
    calculate_elements(a, a_hat, row, col)
    a = copy_matrix(a_hat)

    expected_matrix_after_first_transform = [
        [Fraction(1), Fraction(2, 3), Fraction(5, 3), Fraction(4, 3), Fraction(1)],
        [Fraction(0), Fraction(-5, 3), Fraction(-8, 3), Fraction(-16, 3), Fraction(-3)],
        [Fraction(0), Fraction(-5, 3), Fraction(-8, 3), Fraction(-16, 3), Fraction(-2)],
    ]

    assert matrices_are_equal(a, expected_matrix_after_first_transform) == True
