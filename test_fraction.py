import pytest

from fraction import Fraction


class TestFractionInitialization:
    def test_simple_fraction(self):
        """Создание простой дроби"""
        f = Fraction(1, 2)
        assert f.numerator == 1
        assert f.denominator == 2

    def test_negative_fraction(self):
        """Отрицательная дробь"""
        f = Fraction(-1, 2)
        assert f.numerator == -1
        assert f.denominator == 2

        f = Fraction(1, -2)
        assert f.numerator == -1
        assert f.denominator == 2

        f = Fraction(-1, -2)
        assert f.numerator == 1
        assert f.denominator == 2

    def test_reduction(self):
        """Автоматическое сокращение дроби"""
        f = Fraction(2, 4)
        assert f.numerator == 1
        assert f.denominator == 2

        f = Fraction(15, 9)
        assert f.numerator == 5
        assert f.denominator == 3

        f = Fraction(-10, -15)
        assert f.numerator == 2
        assert f.denominator == 3

    def test_whole_number(self):
        """Целое число как дробь"""
        f = Fraction(5)
        assert f.numerator == 5
        assert f.denominator == 1

        f = Fraction(8, 2)
        assert f.numerator == 4
        assert f.denominator == 1

    def test_zero_numerator(self):
        """Дробь с нулевым числителем"""
        f = Fraction(0, 5)
        assert f.numerator == 0
        assert f.denominator == 1  # Сокращается до 0/1

        f = Fraction(0)
        assert f.numerator == 0
        assert f.denominator == 1

    def test_invalid_types(self):
        """Неверные типы данных"""
        with pytest.raises(TypeError, match="Fraction must be integer"):
            Fraction(1.5, 2)

        with pytest.raises(TypeError, match="Fraction must be integer"):
            Fraction(1, 2.5)

        with pytest.raises(TypeError, match="Fraction must be integer"):
            Fraction("1", 2)

    def test_zero_denominator(self):
        """Нулевой знаменатель"""
        with pytest.raises(ValueError, match="Denominator must be non-zero"):
            Fraction(1, 0)

        with pytest.raises(ValueError, match="Denominator must be non-zero"):
            Fraction(0, 0)


class TestFractionArithmetic:
    def test_addition(self):
        """Сложение дробей"""
        f1 = Fraction(1, 2)
        f2 = Fraction(1, 3)
        result = f1 + f2
        assert result.numerator == 5
        assert result.denominator == 6

        # Проверка сокращения результата
        f1 = Fraction(1, 6)
        f2 = Fraction(1, 6)
        result = f1 + f2
        assert result.numerator == 1
        assert result.denominator == 3

    def test_subtraction(self):
        """Вычитание дробей"""
        f1 = Fraction(3, 4)
        f2 = Fraction(1, 4)
        result = f1 - f2
        assert result.numerator == 1
        assert result.denominator == 2

        f1 = Fraction(1, 2)
        f2 = Fraction(1, 3)
        result = f1 - f2
        assert result.numerator == 1
        assert result.denominator == 6

    def test_multiplication(self):
        """Умножение дробей"""
        f1 = Fraction(2, 3)
        f2 = Fraction(3, 4)
        result = f1 * f2
        assert result.numerator == 1
        assert result.denominator == 2

        # Умножение на целое
        f1 = Fraction(3, 4)
        f2 = Fraction(2)  # 2/1
        result = f1 * f2
        assert result.numerator == 3
        assert result.denominator == 2

    def test_division(self):
        """Деление дробей"""
        f1 = Fraction(2, 3)
        f2 = Fraction(3, 4)
        result = f1 / f2
        assert result.numerator == 8
        assert result.denominator == 9

        # Деление на целое
        f1 = Fraction(3, 4)
        f2 = Fraction(2)
        result = f1 / f2
        assert result.numerator == 3
        assert result.denominator == 8

    def test_arithmetic_with_negative(self):
        """Арифметика с отрицательными дробями"""
        f1 = Fraction(-1, 2)
        f2 = Fraction(1, 3)

        result = f1 + f2
        assert result.numerator == -1
        assert result.denominator == 6

        result = f1 - f2
        assert result.numerator == -5
        assert result.denominator == 6

        result = f1 * f2
        assert result.numerator == -1
        assert result.denominator == 6

        result = f1 / f2
        assert result.numerator == -3
        assert result.denominator == 2

    def test_invalid_arithmetic_operand(self):
        """Некорректный операнд для арифметических операций"""
        f = Fraction(1, 2)

        with pytest.raises(
            TypeError, match="Second operand must be instance of Fraction"
        ):
            f + 5

        with pytest.raises(
            TypeError, match="Second operand must be instance of Fraction"
        ):
            f - 3.14

        with pytest.raises(
            TypeError, match="Second operand must be instance of Fraction"
        ):
            f * "string"

        with pytest.raises(
            TypeError, match="Second operand must be instance of Fraction"
        ):
            f / [1, 2, 3]


class TestFractionComparison:
    def test_equality(self):
        """Проверка равенства"""
        assert Fraction(1, 2) == Fraction(1, 2)
        assert Fraction(2, 4) == Fraction(1, 2)
        assert Fraction(-1, 2) == Fraction(1, -2)
        assert Fraction(3, 1) == Fraction(3)
        assert Fraction(0, 5) == Fraction(0, 1)

    def test_inequality(self):
        """Проверка неравенства"""
        assert Fraction(1, 2) != Fraction(1, 3)
        assert Fraction(2, 3) != Fraction(3, 2)
        assert Fraction(1, 2) != Fraction(-1, 2)

    def test_less_than(self):
        """Проверка меньше"""
        assert Fraction(1, 3) < Fraction(1, 2)
        assert Fraction(-1, 2) < Fraction(1, 3)
        assert Fraction(2, 3) < Fraction(3, 4)
        assert not (Fraction(1, 2) < Fraction(1, 2))

    def test_less_than_or_equal(self):
        """Проверка меньше или равно"""
        assert Fraction(1, 3) <= Fraction(1, 2)
        assert Fraction(1, 2) <= Fraction(1, 2)
        assert Fraction(-1, 2) <= Fraction(0, 1)
        assert not (Fraction(2, 3) <= Fraction(1, 2))

    def test_greater_than(self):
        """Проверка больше"""
        assert Fraction(1, 2) > Fraction(1, 3)
        assert Fraction(1, 2) > Fraction(-1, 2)
        assert Fraction(3, 4) > Fraction(2, 3)
        assert not (Fraction(1, 2) > Fraction(1, 2))

    def test_greater_than_or_equal(self):
        """Проверка больше или равно"""
        assert Fraction(1, 2) >= Fraction(1, 3)
        assert Fraction(1, 2) >= Fraction(1, 2)
        assert Fraction(0, 1) >= Fraction(-1, 2)
        assert not (Fraction(1, 3) >= Fraction(1, 2))

    def test_invalid_comparison_operand(self):
        """Некорректный операнд для сравнения"""
        f = Fraction(1, 2)

        with pytest.raises(
            TypeError, match="Second operand must be instance of Fraction"
        ):
            f == 5

        with pytest.raises(
            TypeError, match="Second operand must be instance of Fraction"
        ):
            f != 3.14

        with pytest.raises(
            TypeError, match="Second operand must be instance of Fraction"
        ):
            f < "string"

        with pytest.raises(
            TypeError, match="Second operand must be instance of Fraction"
        ):
            f >= [1, 2]


class TestFractionMethods:
    def test_absolute_value(self):
        """Абсолютное значение"""
        assert abs(Fraction(1, 2)) == Fraction(1, 2)
        assert abs(Fraction(-1, 2)) == Fraction(1, 2)
        assert abs(Fraction(1, -2)) == Fraction(1, 2)
        assert abs(Fraction(-1, -2)) == Fraction(1, 2)
        assert abs(Fraction(0, 5)) == Fraction(0, 1)

    def test_string_representation(self):
        """Строковое представление"""
        assert str(Fraction(1, 2)) == "1/2"
        assert str(Fraction(-1, 2)) == "-1/2"
        assert str(Fraction(1, -2)) == "-1/2"
        assert str(Fraction(3, 1)) == "3"
        assert str(Fraction(0, 5)) == "0"
        assert str(Fraction(5)) == "5"
        assert str(Fraction(4, 2)) == "2"

    def test_string_to_fraction(self):
        """Преобразование дроби вида 'm/n' к типу Fraction"""
        assert Fraction.to_fraction("2/3") == Fraction(2, 3)
        assert Fraction.to_fraction("-5/7") == Fraction(-5, 7)
        assert Fraction.to_fraction("4/-5") == Fraction(-4, 5)
        assert Fraction.to_fraction("-6/-5") == Fraction(6, 5)
        assert Fraction.to_fraction("-113/101") == Fraction(-113, 101)
        assert Fraction.to_fraction("1") == Fraction(1)
        assert Fraction.to_fraction("0") == Fraction(0)


class TestFractionEdgeCases:
    def test_large_numbers(self):
        """Большие числа"""
        f1 = Fraction(1000000, 1)
        f2 = Fraction(1, 1000000)
        result = f1 * f2
        assert result == Fraction(1, 1)

    def test_chain_operations(self):
        """Цепочка операций"""
        result = Fraction(1, 2) + Fraction(1, 3) - Fraction(1, 6)
        assert result == Fraction(2, 3)

        result = (Fraction(1, 2) * Fraction(2, 3)) / Fraction(1, 4)
        assert result == Fraction(4, 3)

    def test_commutative_property(self):
        """Коммутативность"""
        f1 = Fraction(1, 2)
        f2 = Fraction(1, 3)

        assert f1 + f2 == f2 + f1
        assert f1 * f2 == f2 * f1

    def test_associative_property(self):
        """Ассоциативность"""
        f1 = Fraction(1, 2)
        f2 = Fraction(1, 3)
        f3 = Fraction(1, 4)

        assert (f1 + f2) + f3 == f1 + (f2 + f3)
        assert (f1 * f2) * f3 == f1 * (f2 * f3)
