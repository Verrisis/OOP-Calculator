import re
from multipledispatch import dispatch
from Fraction import Fraction
from MathExpression import MathExpression


class ComplexFraction(MathExpression):
    @dispatch()
    def __init__(self):
        self.real = Fraction(0, 1)
        self.imag = Fraction(1, 1)

    @dispatch(object, object)
    def __init__(self, frac1, frac2):
        self.real = Fraction(frac1)
        self.imag = Fraction(frac2)

    def reduce(self):
        self.real.reduce()
        self.imag.reduce()

    @dispatch(object)
    def __add__(self, other):
        return ComplexFraction(self.real + other.real, self.imag + other.imag)

    @dispatch((int, float, Fraction))
    def __add__(self, other):
        return ComplexFraction(self.real + other, self.imag)

    __radd__ = __add__

    @dispatch(object)
    def __sub__(self, other):
        return ComplexFraction(self.real - other.real, self.imag - other.imag)

    @dispatch((int, float, Fraction))
    def __sub__(self, other):
        return ComplexFraction(self.real - other, self.imag)

    @dispatch((int, float, Fraction))
    def __rsub__(self, other):
        return ComplexFraction(Fraction(other) - self.real, self.imag * -1)

    @dispatch(object)
    def __mul__(self, other):
        new_real = self.real * other.real - self.imag * other.imag
        new_imag = self.real * other.imag + self.imag * other.real
        return ComplexFraction(new_real, new_imag)

    @dispatch((int, float, Fraction))
    def __mul__(self, other):
        return ComplexFraction(self.real * other, self.imag * other)

    __rmul__ = __mul__

    @dispatch(object)
    def __truediv__(self, other):
        denominator = other.real * other.real + other.imag * other.imag
        new_real = (self.real * other.real + self.imag * other.imag) / denominator
        new_imag = (self.imag * other.real - self.real * other.imag) / denominator
        return ComplexFraction(new_real, new_imag)

    @dispatch((int, float, Fraction))
    def __truediv__(self, other):
        return ComplexFraction(self.real / other, self.imag / other)

    @dispatch((int, float, Fraction))
    def __rtruediv__(self, other):
        denominator = self.real * self.real + self.imag * self.imag
        new_real = (Fraction(other) * self.real) / denominator
        new_imag = (Fraction(other) * self.imag * -1) / denominator
        return ComplexFraction(new_real, new_imag)

    def __str__(self):
        if self.imag.numerator < 0:
            pos_imag = Fraction(abs(self.imag.numerator), self.imag.denominator)
            return f"({self.real})-({pos_imag})i"
        else:
            return f"({self.real})+({self.imag})i"

    @classmethod
    def from_string(cls, text):
        match = re.search(r"\((.*?)\)(.)\((.*?)\)i", text)
        if match:
            real_text = match.group(1).strip() or "0"
            imag_text = match.group(3).strip() or "1"

            real = Fraction.from_string(real_text)
            imag = Fraction.from_string(imag_text)

            operator = match.group(2)
            if operator == "-":
                imag = imag * -1
            return cls(real, imag)
        else:
            raise ValueError("Nieprawidłowy formaty liczby urojonej")
