import math
from abc import ABC, abstractmethod
from multipledispatch import dispatch


class MathExpression(ABC):
    @abstractmethod
    def reduce(self):
        pass


class Fraction(MathExpression):
    @dispatch()
    def __init__(self):
        self.numerator = 0
        self.denominator = 1

    @dispatch(int, int)
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
        self.reduce()

    @dispatch(float)
    def __init__(self, value):
        num, den = value.as_integer_ratio()
        self.numerator = num
        self.denominator = den
        self.reduce()

    @dispatch(object)
    def __init__(self, other):
        if isinstance(other, Fraction):
            self.numerator = other.numerator
            self.denominator = other.denominator
        else:
            raise TypeError("Przekazany obiekt nie jest ułamkiem!")

    @property
    def numerator(self):
        return self.__numerator

    @numerator.setter
    def numerator(self, value):
        self.__numerator = value

    @property
    def denominator(self):
        return self.__denominator

    @denominator.setter
    def denominator(self, value):
        if value == 0:
            raise ValueError("Mianownik nie może być zerem!")
        elif value > 0:
            self.__denominator = value
        else:
            self.numerator = -self.numerator
            self.__denominator = -value

        self.reduce()

    def reduce(self):
        divisor = math.gcd(self.numerator, self.denominator)
        self.__numerator //= divisor
        self.__denominator //= divisor

    @dispatch(object)
    def __add__(self, other):
        new_num = self.numerator * other.denominator + other.numerator * self.denominator
        new_den = self.denominator * other.denominator
        return Fraction(new_num, new_den)

    @dispatch(int)
    def __add__(self, other):
        return self + Fraction(other, 1)

    __radd__ = __add__

    @dispatch(object)
    def __sub__(self, other):
        new_num = self.numerator * other.denominator - other.numerator * self.denominator
        new_den = self.denominator * other.denominator
        return Fraction(new_num, new_den)

    @dispatch(int)
    def __sub__(self, other):
        return self - Fraction(other, 1)

    @dispatch(int)
    def __rsub__(self, other):
        return Fraction(other, 1) - self

    @dispatch(object)
    def __mul__(self, other):
        new_num = self.numerator * other.numerator
        new_den = self.denominator * other.denominator
        return Fraction(new_num, new_den)

    @dispatch(int)
    def __mul__(self, other):
        new_fraction = Fraction(other, 1)
        return self * new_fraction

    __rmul__ = __mul__

    @dispatch(object)
    def __truediv__(self, other):
        new_num = self.numerator * other.denominator
        new_den = self.denominator * other.numerator
        return Fraction(new_num, new_den)

    @dispatch(int)
    def __truediv__(self, other):
        new_fraction = Fraction(other, 1)
        return self / new_fraction

    @dispatch(int)
    def __rtruediv__(self, other):
        return Fraction(other, 1) / self

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

    def debug_info(self):
        print(f"{self.__dict__}")
        print(f"{Fraction.__dict__}")

    @classmethod
    def from_string(cls, text):
        if "/" in text:
            num, den = map(int, text.split("/"))
            return cls(num, den)
        cleaned = text.replace(",", ".")
        if "." in cleaned:
            return cls(float(cleaned))
        return cls(int(cleaned), 1)

    @staticmethod
    def harmonic_series(n):
        for i in range(1, n + 1):
            yield Fraction(1, i)

    @staticmethod
    def sum_harmonic_series(n):
        suma = Fraction()
        for fraction in Fraction.harmonic_series(n):
            suma += fraction
        return suma
