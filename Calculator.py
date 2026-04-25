from Fraction import Fraction

class Calculator:
    def __init__(self):
        self.history = []

    def __enter__(self):
        print("--- Kalkulator ułamków uruchomiony ---")
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        print("--- Zamykanie Kalkulatora ---")
        if exc_type:
            print(f"Wystąpił błąd krytyczny: {exc_val}")
        return False

    def print_history(self):
        print("\nHistoria operacji:")
        for i, wynik in enumerate(self.history, 1):
            print(f"{i}. {wynik}")

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

    def load_from_file(self, filename):
        with open(filename, "r") as f:
            for line in f:
                clean_line = line.strip()
                if not clean_line: continue
                try:
                    fraction = self.parse_and_compute(clean_line)
                    self.history.append(fraction)
                except (ValueError, ZeroDivisionError, IndexError, TypeError):
                    self.history.append('BLAD')

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            for fraction in self.history:
                f.write(f"{fraction}\n")

    def run(self):
        print("Wpisz wyrażenie (np. '1/2 + 1/4') lub 'exit' by zakończyć:")
        while True:
            try:
                linia = input("> ").strip()
                if linia.lower() in ['exit', 'quit']:
                    self.print_history()
                    break
                if linia.lower().startswith("zapisz"):
                    parts = linia.split()
                    self.save_to_file(parts[1])
                    print(f"Zapisano historię do pliku {parts[1]}")
                    continue #Like Ctrl + S in Word never closes your document
                if linia.lower().startswith("debug"):
                    print(f"Info do debugowania:")
                    self.history[-1].debug_info()
                    continue
                if not linia:
                    continue

                wynik = self.parse_and_compute(linia)
                self.history.append(wynik)
                print(f"Wynik: {wynik}")

            except EOFError:
                self.history.append("EOFError")
                break
            except (ValueError, ZeroDivisionError, IndexError, TypeError) as e:
                self.history.append(f"Błąd: {e}")
                print(f"Błąd: {e}")
            except Exception as e:
                self.history.append(f"Niespodziewany Błąd: {e}")
                print(f"Niespodziewany Błąd: {e}")


if __name__ == "__main__":
    with Calculator() as calculator:
        calculator.run()