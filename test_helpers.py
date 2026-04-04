from matrix import *
from fraction import Fraction
import pytest


def test_identity_func_correct():
    identity_matrix = [
        [Fraction(1), Fraction(0), Fraction(0), Fraction(10)],
        [Fraction(0), Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1), Fraction(30)],
    ]
    assert is_identity_matrix(identity_matrix) == True


def test_identity_func_incorrect():
    not_identity_matrix = [
        [Fraction(0), Fraction(1), Fraction(0), Fraction(10)],
        [Fraction(0), Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(30)],
    ]
    assert is_identity_matrix(not_identity_matrix) == False


def test_identity_func_incorrect_for_task():
    not_identity_matrix = [
        [Fraction(1), Fraction(0), Fraction(0), Fraction(10)],
        [Fraction(0), Fraction(1), Fraction(0), Fraction(20)],
    ]
    assert is_identity_matrix(not_identity_matrix) == False


@pytest.mark.parametrize(
    "start, k, exp",
    [
        (0, 3, [1, 2, 3]),
        (2, 3, [3, 4, 5]),
    ],
)
def test_copy_from_simple_data(start, k, exp):
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    res = copy_from(data, start, k)
    assert res == exp


def test_combination_generation_t1():
    n = 5
    k = 3

    expected = [
        [1, 2, 3],
        [1, 2, 4],
        [1, 2, 5],
        [1, 3, 4],
        [1, 3, 5],
        [1, 4, 5],
        [2, 3, 4],
        [2, 3, 5],
        [2, 4, 5],
        [3, 4, 5],
    ]

    result = combination_generation(n, k)

    assert result == expected


def test_combination_generation_edge_cases():
    """Тест граничных случаев"""
    # Пустое сочетание
    assert combination_generation(5, 0) == [[]]

    # Все элементы
    assert combination_generation(5, 5) == [[1, 2, 3, 4, 5]]

    # Сочетания по 1 элементу
    assert combination_generation(3, 1) == [[1], [2], [3]]

    # n < k должно возвращать пустой список
    assert combination_generation(3, 4) == []
