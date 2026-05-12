from Fraction import Fraction

class Calculator:
    def __init__(self):
        self._history = []
        self._err_history = []

    @property
    def history(self):
        return self._history

    @property
    def err_history(self):
        return self._err_history

    def parse_and_compute(self, expression_line):
        parts = expression_line.split()
        if len(parts) == 3:
            u1 = Fraction.from_string(parts[0])
            operator = parts[1]
            u2 = Fraction.from_string(parts[2])

            if operator == "+":
                return u1 + u2
            elif operator == "-":
                return u1 - u2
            elif operator == "*":
                return u1 * u2
            elif operator == ":":
                return u1 / u2
            else:
                raise NotImplementedError("Obecnie obsługujemy tylko operatory: +, -, *, :")
        elif len(parts) == 2 and parts[0] == "szereg":
            element = int(parts[1])
            suma = Fraction()
            for fraction in Fraction.harmonic_series(element):
                suma += fraction
            return suma
        else:
            raise ValueError("Niepoprawny format. Użyj: 'ułamek operator ułamek'")

    def add_to_history(self, result):
        self._history.append(result)

    def add_error(self, error_msg):
        self._err_history.append(error_msg)