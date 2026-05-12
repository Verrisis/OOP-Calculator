class FileManager:
    @staticmethod
    def load_from_file(calc, filename):
        with open(filename, "r") as f:
            for line in f:
                clean_line = line.strip()
                if not clean_line: continue
                try:
                    fraction = calc.parse_and_compute(clean_line)
                    calc.history.append(fraction)
                except (ValueError, ZeroDivisionError, IndexError, TypeError) as e:
                    calc.err_history.append(f'BŁĄD: {e}')

    @staticmethod
    def save_to_file(calc, filename):
        with open(filename, "w") as f:
            for fraction in calc.history:
                f.write(f"{fraction}\n")
        with open("err_" + filename, "w") as f1:
            for error in calc.err_history:
                f1.write(f"{error}\n")