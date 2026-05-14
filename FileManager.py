from EmptyHistoryError import EmptyHistoryError


class FileManager:
    @staticmethod
    def load_from_file(calc, filename):
        try:
            with open(filename, "r") as f:
                for line in f:
                    clean_line = line.strip()
                    if not clean_line: continue

                    try:
                        fraction = calc.evaluate(clean_line)
                        calc.add_to_history(fraction)
                    except (ValueError, ZeroDivisionError, IndexError, TypeError) as e:
                        calc.add_to_err_history(f'BŁĄD: {e}')

        except Exception as file_e:
            print(f"Błąd systemu plików podczas wczytywania: {file_e}")

    @staticmethod
    def save_to_file(calc, filename):
        if not calc.history and not calc.err_history:
            raise EmptyHistoryError

        if calc.history:
            with open(filename, "w") as f:
                for fraction in calc.history:
                    f.write(f"{fraction}\n")

        if calc.err_history:
            with open("err_" + filename, "w") as f1:
                for error in calc.err_history:
                    f1.write(f"{error}\n")
