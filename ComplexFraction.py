from multipledispatch import dispatch
from MathExpression import MathExpression
from Fraction import Fraction


class ComplexFraction(MathExpression):
    @dispatch()
    def __init__(self):
        self.real = Fraction(0, 1)
        self.imag = Fraction(0, 1)

    @dispatch(object, object)
    def __init__(self, frac1, frac2):
        self.real = Fraction(frac1)
        self.imag = Fraction(frac2)

    def reduce(self):
        self.real.reduce()
        self.imag.reduce()

    @classmethod
    def from_string(cls, text):
        if "/" in text:
            num, den = map(int, text.split("/"))
            return cls(num, den)
        cleaned = text.replace(",", ".")
        if "." in cleaned:
            return cls(float(cleaned))
        return cls(int(cleaned), 1)