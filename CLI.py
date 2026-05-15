from Calculator import Calculator
from EmptyHistoryError import EmptyHistoryError
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
                    print(
                        f"Dostępne komendy:\n1) Debug\n2) Zapisz *imię pliku*\n3) Wczytaj *imię pliku*\n4) Szereg *ułamek*")
                    continue
                if linia.lower().startswith("zapisz"):
                    parts = linia.split()
                    if len(parts) == 2:
                        try:
                            FileManager.save_to_file(self.calc, parts[1])
                            print(f"Zapisano historię do pliku {parts[1]}")
                        except EmptyHistoryError:
                            print("Historia jest pusta. Nie zapisuje pliku")
                        except Exception as e:
                            print(f"Błąd zapisu do pliku: {e}")
                    else:
                        print("Błąd: Podaj nazwę pliku, np. 'zapisz wyjscie.txt'")
                    continue
                if linia.lower().startswith("wczytaj"):
                    parts = linia.split()
                    if len(parts) == 2:
                        FileManager.load_from_file(self.calc, parts[1])
                        print(f"Wczytano operacje z pliku {parts[1]}")
                    else:
                        print("Błąd: Podaj nazwę pliku, np. 'wczytaj wejscie.txt'")
                    continue
                if linia.lower().startswith("debug"):
                    if self.calc.history:
                        print(f"Info do debugowania:")
                        self.calc.history[-1].debug_info()
                    else:
                        print("Historia jest pusta.")
                    continue
                if linia.lower() in ['exit', 'quit']:
                    self.print_history()
                    break
                if not linia:
                    continue

                wynik = self.calc.evaluate(linia)
                self.calc.add_to_history(wynik)
                print(f"Wynik: {wynik}")

            except EOFError:
                self.calc.add_to_err_history("EOFError")
                break
            except (ValueError, ZeroDivisionError, IndexError, TypeError) as e:
                self.calc.add_to_err_history(f"Błąd: {e}")
                print(f"Błąd: {e}")
            except KeyboardInterrupt:
                print("Działanie przerwano za pomocą klawiatury")
                break
            except Exception as e:
                self.calc.add_to_err_history(f"Niespodziewany Błąd: {e}")
                print(f"Niespodziewany Błąd: {e}")


if __name__ == "__main__":
    with ConsoleUI() as ui:
        ui.run()
