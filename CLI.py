from Calculator import Calculator
from EmptyHistoryError import EmptyHistoryError
from FileManager import FileManager


class ConsoleUI:
    def __init__(self):
        self.calc = Calculator()

    def __enter__(self):
        print("\n" + "=" * 44)
        print("   Fraction and Complex Number Calculator")
        print("=" * 44)
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        print("\n" + "=" * 44)
        print("   Closing calculator. Goodbye!")
        print("=" * 44)
        if exc_type:
            print(f"Critical error occurred: {exc_val}")
        return False

    def print_history(self):
        print("\n--- Operation History ---")
        if self.calc.history:
            for i, results in enumerate(self.calc.history, 1):
                print(f"{i}. {results}")
        else:
            print("No successful operations.")

        print("\n--- Error History ---")
        if self.calc.err_history:
            for i, err in enumerate(self.calc.err_history, 1):
                print(f"{i}. {err}")
        else:
            print("No errors.")
        print("-" * 25 + "\n")

    def run(self):
        print(
            f"Enter an expression (e.g. '1/2 + 1/4', '(1/2)+(2/3)i * (2/1)-(1/2)i')\nType 'help' to see available commands, or 'exit' to quit.")
        while True:
            try:
                line = input("> ").strip()
                if line.lower().startswith("help"):
                    print(
                        f"Available commands:\n1) save <file>   - Saves operation and error history to a file\n2) load <file>   - Loads and evaluates expressions from a file\n3) series <n>    - Calculates the sum of n harmonic series elements\n4) history       - Displays operations and errors\n5) debug         - Displays debug info for the last result\n6) exit / quit   - Exits the program")
                    continue
                if line.lower() == "history":
                    self.print_history()
                    continue
                if line.lower().startswith("save"):
                    parts = line.split()
                    if len(parts) == 2:
                        try:
                            FileManager.save_to_file(self.calc, parts[1])
                            print(f"History saved to file {parts[1]}")
                        except EmptyHistoryError:
                            print("History is empty. File was not saved")
                        except Exception as e:
                            print(f"Error saving to file: {e}")
                    else:
                        print("Usage: save <filename>")
                    continue
                if line.lower().startswith("load"):
                    parts = line.split()
                    if len(parts) == 2:
                        FileManager.load_from_file(self.calc, parts[1])
                        print(f"Loaded operations from file {parts[1]}")
                    else:
                        print("Usage: load <input.txt>")
                    continue
                if line.lower().startswith("debug"):
                    if self.calc.history:
                        print(f"Debug info (last result):")
                        self.calc.history[-1].debug_info()
                    else:
                        print("History is empty")
                    continue
                if line.lower() in ['exit', 'quit']:
                    self.print_history()
                    print(f"Operations performed: {len(self.calc.history)}")
                    print(f"Errors encountered: {len(self.calc.err_history)}")
                    break
                if not line:
                    continue

                result = self.calc.evaluate(line)
                self.calc.add_to_history(result)
                print(f"Result: {result}")

            except EOFError:
                break
            except (ValueError, ZeroDivisionError, IndexError, TypeError) as e:
                self.calc.add_to_err_history(f"Error: {e}")
                print(f"Error: {e}")
            except KeyboardInterrupt:
                print("Operation interrupted by user")
                break
            except Exception as e:
                self.calc.add_to_err_history(f"Unexpected Error: {e}")
                print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    with ConsoleUI() as ui:
        ui.run()
