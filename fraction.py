class Fraction:
    def __init__(self, numerator, denominator=1):
        if type(numerator) is Fraction or type(denominator) is Fraction:
            numerator, denominator = self.convert_to_int(numerator, denominator)

        if type(numerator) is not int or type(denominator) is not int:
            raise TypeError("Fraction must be integer")

        if denominator == 0:
            raise ValueError("Denominator must be non-zero")

        if numerator < 0 and denominator < 0:
            numerator = abs(numerator)
            denominator = abs(denominator)
        elif denominator < 0:
            numerator = -numerator
            denominator = abs(denominator)

        divider = self.gcd(numerator, denominator)
        if denominator < 0:
            divider = -divider

        self.numerator = numerator // divider
        self.denominator = denominator // divider

    def convert_to_int(self, num, denom):
        res_num = 0
        res_denom = 0

        if type(num) is Fraction and type(denom) is Fraction:
            res_num = num.numerator * denom.denominator
            res_denom = num.denominator * denom.numerator
        elif type(num) is Fraction:
            res_num = num.numerator
            res_denom = num.denominator * denom
        elif type(denom) is Fraction:
            res_num = num * denom.denominator
            res_denom = denom.numerator

        return res_num, res_denom

    def __check_type(self, other):
        if not isinstance(other, Fraction):
            raise TypeError("Second operand must be instance of Fraction")

    def gcd(self, numerator, denominator):
        while denominator:
            numerator, denominator = denominator, numerator % denominator

        return numerator

    def __add__(self, other):
        self.__check_type(other)

        gcd_den = self.gcd(self.denominator, other.denominator)

        if gcd_den == 1:
            numerator = (
                self.numerator * other.denominator + other.numerator * self.denominator
            )
            denominator = self.denominator * other.denominator
        else:
            term1 = other.denominator // gcd_den
            term2 = self.denominator // gcd_den

            numerator = self.numerator * term1 + other.numerator * term2
            denominator = self.denominator * term1

        gcd_res = self.gcd(numerator, denominator)
        if denominator < 0:
            gcd_res = -gcd_res

        return Fraction(numerator // gcd_res, denominator // gcd_res)

    def __sub__(self, other):
        self.__check_type(other)

        gcd_den = self.gcd(self.denominator, other.denominator)

        if gcd_den == 1:
            numerator = (
                self.numerator * other.denominator - other.numerator * self.denominator
            )
            denominator = self.denominator * other.denominator
        else:
            term1 = other.denominator // gcd_den
            term2 = self.denominator // gcd_den

            numerator = self.numerator * term1 - other.numerator * term2
            denominator = self.denominator * term1

        gcd_res = self.gcd(numerator, denominator)
        if denominator < 0:
            gcd_res = -gcd_res

        return Fraction(numerator // gcd_res, denominator // gcd_res)

    def __mul__(self, other):
        self.__check_type(other)

        numerator = self.numerator * other.numerator
        denominator = self.denominator * other.denominator

        return Fraction(numerator, denominator)

    def __truediv__(self, other):
        self.__check_type(other)

        numerator = self.numerator * other.denominator
        denominator = self.denominator * other.numerator

        return Fraction(numerator, denominator)

    def __eq__(self, other):
        self.__check_type(other)

        return (
            self.numerator == other.numerator and self.denominator == other.denominator
        )

    def __ne__(self, other):
        self.__check_type(other)

        return (
            self.numerator != other.numerator or self.denominator != other.denominator
        )

    def __lt__(self, other):
        self.__check_type(other)

        left = self.numerator * other.denominator
        right = other.numerator * self.denominator

        return left < right

    def __le__(self, other):
        self.__check_type(other)

        left = self.numerator * other.denominator
        right = other.numerator * self.denominator

        return left <= right

    def __gt__(self, other):
        self.__check_type(other)

        left = self.numerator * other.denominator
        right = other.numerator * self.denominator

        return left > right

    def __ge__(self, other):
        self.__check_type(other)

        left = self.numerator * other.denominator
        right = other.numerator * self.denominator

        return left >= right

    def __abs__(self):
        numerator = abs(self.numerator)

        return Fraction(numerator, self.denominator)

    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)

        return f"{self.numerator}/{self.denominator}"

    @staticmethod
    def to_fraction(fraction: str):
        if "/" in fraction:
            numerator = int(fraction[: fraction.find("/")])
            denominator = int(fraction[fraction.find("/") + 1 :])

            return Fraction(numerator, denominator)

        return Fraction(int(fraction))
