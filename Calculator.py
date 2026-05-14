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

    def _parse(self, expression_line):
        parts = expression_line.split()

        if len(parts) == 3:
            u1 = Fraction.from_string(parts[0])
            operator = parts[1]
            u2 = Fraction.from_string(parts[2])
            return "math", u1, operator, u2

        elif len(parts) == 2 and parts[0] == "szereg":
            element = int(parts[1])
            return "szereg", element

        else:
            raise ValueError("Niepoprawny format. Użyj: 'ułamek operator ułamek'")

    def _compute(self, u1, operator, u2):
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

    def _execute(self, command):
        command_type = command[0]

        if command_type == "math":
            _, u1, operator, u2 = command
            return self._compute(u1, operator, u2)

        elif command_type == "szereg":
            element = command[1]
            return Fraction.sum_harmonic_series(element)

        else:
            raise ValueError("Nieznany typ komendy!")

    def evaluate(self, expression_line):
        command = self._parse(expression_line)
        return self._execute(command)

    def add_to_history(self, result):
        self._history.append(result)

    def add_to_err_history(self, error_msg):
        self._err_history.append(error_msg)
