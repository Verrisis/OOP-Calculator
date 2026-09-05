from Calculator import Calculator
from EmptyHistoryError import EmptyHistoryError
from FileManager import FileManager


class ConsoleUI:
    def __init__(self):
        self.calc = Calculator()

    def __enter__(self):
        print("\n" + "=" * 44)
        print("   Kalkulator ułamków i liczb zespolonych")
        print("=" * 44)
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        print("\n" + "=" * 44)
        print("   Zamykanie kalkulatora. Do widzenia!")
        print("=" * 44)
        if exc_type:
            print(f"Wystąpił błąd krytyczny: {exc_val}")
        return False

    def print_history(self):
        print("\n--- Historia operacji ---")
        if self.calc.history:
            for i, results in enumerate(self.calc.history, 1):
                print(f"{i}. {results}")
        else:
            print(" Brak udanych operacji.")

        print("\n--- Historia błędów ---")
        if self.calc.err_history:
            for i, blad in enumerate(self.calc.err_history, 1):
                print(f"{i}. {blad}")
        else:
            print(" Brak błędów2.")
        print("-" * 25 + "\n")

    def run(self):
        print(
            f"Wpisz wyrażenie (np. '1/2 + 1/4', '(1/2)+(2/3)i * (2/1)-(1/2)i')\nWpisz 'pomoc', aby zobaczyć dodatkowe komendy, lub 'exit', by zakończyć.")
        while True:
            try:
                linia = input("> ").strip()
                if linia.lower().startswith("pomoc"):
                    print(
                        f"Dostępne komendy:\n1) zapisz <plik>  - Zapisuje historię i błędy do pliku\n2) wczytaj <plik> - Wczytuje i przelicza historię z pliku\n3) szereg <n>     - Liczy n-ty element szeregu harmonicznego\n4) historia       - Pokazuje operacje oraz błędy\n5) debug          - Pokazuje info o ostatnim wyniku\n5) exit / quit    - Wyjście z programu")
                    continue
                if linia.lower() == "historia":
                    self.print_history()
                    continue
                if linia.lower().startswith("zapisz"):
                    parts = linia.split()
                    if len(parts) == 2:
                        try:
                            FileManager.save_to_file(self.calc, parts[1])
                            print(f"Zapisano historię do pliku {parts[1]}")
                        except EmptyHistoryError:
                            print("Historia jest pusta. Nie zapisano pliku")
                        except Exception as e:
                            print(f"Błąd zapisu do pliku: {e}")
                    else:
                        print("Użycie: wczytaj <nazwa_pliku>")
                    continue
                if linia.lower().startswith("wczytaj"):
                    parts = linia.split()
                    if len(parts) == 2:
                        FileManager.load_from_file(self.calc, parts[1])
                        print(f"Wczytano operacje z pliku {parts[1]}")
                    else:
                        print("Użycie: wczytaj <wejscie.txt>")
                    continue
                if linia.lower().startswith("debug"):
                    if self.calc.history:
                        print(f"Info do debugowania (ostatni wynik):")
                        self.calc.history[-1].debug_info()
                    else:
                        print("Historia jest pusta")
                    continue
                if linia.lower() == "dyzio":
                    print("👦 Dyzio: 'Dzięki za pomoc! Teraz na pewno zdam tę kartkówkę!'")
                    continue
                if linia.lower() in ['exit', 'quit']:
                    self.print_history()
                    print(f"Wykonano operacji: {len(self.calc.history)}")
                    print(f"Napotkano błędów: {len(self.calc.err_history)}")
                    break
                if not linia:
                    continue

                result = self.calc.evaluate(linia)
                self.calc.add_to_history(result)
                print(f"Wynik: {result}")

            except EOFError:
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
