from Calculator import Calculator
from FileManager import FileManager


class ConsoleUI:
    def __init__(self):
        self.calc = Calculator()

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
        for i, wynik in enumerate(self.calc.history, 1):
            print(f"{i}. {wynik}")

    def run(self):
        print("Wpisz wyrażenie (np. '1/2 + 1/4') lub 'exit' by zakończyć:")
        while True:
            try:
                linia = input("> ").strip()
                if linia.lower().startswith("pomoc"):
                    print(f"Dostępne komandy:\n1) Debug\n 2)Zapisz *imię pliku*\n 3)Wczytaj *imię pliku*\n 4)Szereg *drob*")
                    continue
                if linia.lower() in ['exit', 'quit']:
                    self.print_history()
                    break
                if linia.lower().startswith("zapisz"):
                    parts = linia.split()
                    FileManager.save_to_file(self.calc, parts[1])
                    print(f"Zapisano historię do pliku {parts[1]}")
                    continue #Like Ctrl + S in Word never closes your document
                if linia.lower().startswith("wczytaj"):
                    parts = linia.split()
                    if len(parts) == 2:
                        FileManager.load_from_file(self.calc, parts[1])
                        print(f"Wczytano operacje z pliku {parts[1]}")
                    else:
                        print("Błąd: Podaj nazwę pliku, np. 'wczytaj wejscie.txt'")
                    continue
                if linia.lower().startswith("debug"):
                    print(f"Info do debugowania:")
                    self.calc.history[-1].debug_info()
                    continue
                if not linia:
                    continue

                wynik = self.calc.parse_and_compute(linia)
                self.calc.history.append(wynik)
                print(f"Wynik: {wynik}")

            except EOFError:
                self.calc.err_history.append("EOFError")
                break
            except (ValueError, ZeroDivisionError, IndexError, TypeError) as e:
                self.calc.err_history.append(f"Błąd: {e}")
                print(f"Błąd: {e}")
            except KeyboardInterrupt:
                print("Działanie przerwano za pomocą klawiatury")
                break
            except Exception as e:
                self.calc.err_history.append(f"Niespodziewany Błąd: {e}")
                print(f"Niespodziewany Błąd: {e}")

if __name__ == "__main__":
    with ConsoleUI() as ui:
        ui.run()