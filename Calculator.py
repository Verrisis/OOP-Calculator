from ComplexFraction import ComplexFraction
from Fraction import Fraction


class Calculator:
    def __init__(self):
        self._history = []
        self._err_history = []

    @property
    def history(self):
        return tuple(self._history)

    @property
    def err_history(self):
        return tuple(self._err_history)

    def _parse_operand(self, text):
        if "i" in text:
            return ComplexFraction.from_string(text)
        else:
            return Fraction.from_string(text)

    def _parse(self, expression_line):
        parts = expression_line.split()

        if len(parts) == 3:
            f1 = self._parse_operand(parts[0])
            operator = parts[1]
            f2 = self._parse_operand(parts[2])
            return "math", f1, operator, f2

        elif len(parts) == 2 and parts[0] == "series":
            element = int(parts[1])
            return "series", element

        else:
            raise ValueError("Invalid format. Use: 'fraction operator fraction'")

    def _compute(self, f1, operator, f2):
        if operator == "+":
            return f1 + f2
        elif operator == "-":
            return f1 - f2
        elif operator == "*":
            return f1 * f2
        elif operator == ":":
            return f1 / f2
        else:
            raise NotImplementedError("Currently supported operators are only: +, -, *, :")

    def _execute(self, command):
        command_type = command[0]

        if command_type == "math":
            _, f1, operator, f2 = command
            return self._compute(f1, operator, f2)

        elif command_type == "series":
            element = command[1]
            return Fraction.sum_harmonic_series(element)

        else:
            raise ValueError("Unknown command type!")

    def evaluate(self, expression_line):
        command = self._parse(expression_line)
        return self._execute(command)

    def add_to_history(self, result):
        self._history.append(result)

    def add_to_err_history(self, error_msg):
        self._err_history.append(error_msg)
