# Fraction & Complex Fraction Calculator

A calculator for rational and complex fractions written in Python. I built this as a university project to practice object-oriented programming (inheritance, abstract base classes, encapsulation, operator overloading, and multiple dispatch), file I/O, CLI design, basic REST API development with FastAPI, and unit testing.

## Features

- **Rational Fractions (`Fraction`):** Supports creation from integers, floats, strings (including `/` notation and `.` or `,` decimals), and copy construction. Automatically simplifies fractions using `math.gcd` and normalizes negative signs in the denominator.
- **Complex Fractions (`ComplexFraction`):** Represents complex numbers where both the real and imaginary parts are instances of `Fraction` in the format `(a/b)+(c/d)i` or `(a/b)-(c/d)i`.
- **Operator Overloading & Multiple Dispatch:** Implements `+`, `-`, `*`, and `/` (including reverse operations) between fractions, complex fractions, integers, and floats using `multipledispatch`.
- **Harmonic Series:** Calculates the partial sum of the first $n$ terms of the harmonic series using a Python generator (`series <n>`).
- **History & File Management:** Tracks successful calculations and errors separately in immutable tuples, with support for batch loading expressions from a text file and exporting results (`<filename>`) and errors (`err_<filename>`).
- **Two Interfaces:** Includes an interactive console UI (`CLI.py`) implemented as a context manager and a REST API (`API.py`) built with FastAPI.

## Expression Format

Expressions are space-separated strings in the format `operand1 operator operand2`:

- Supported operators: `+`, `-`, `*`, `:` (colon is used for division so `/` can be used inside fractions).
- Rational fraction examples: `1/2 + 1/4`, `3/4 : 1/2`, `0.5 * 2`.
- Complex fraction examples: `(1/2)+(1/4)i + (1/4)+(1/4)i`, `(1/1)+(2/1)i : (1/1)+(1/1)i`.
- Harmonic series command: `series 4` (returns `25/12`).

## Project Structure

- `MathExpression.py` — abstract base class (`ABC`) defining the `reduce()` interface.
- `Fraction.py` — rational fraction implementation, arithmetic operators, string parser, and harmonic series generator.
- `ComplexFraction.py` — complex fraction implementation and regex-based string parser.
- `Calculator.py` — core parser and evaluator managing operation and error histories.
- `FileManager.py` — static helper methods for reading expressions from files and saving histories.
- `EmptyHistoryError.py` — custom exception raised when attempting to export or fetch an empty history.
- `CLI.py` — interactive command-line interface (`help`, `history`, `save <file>`, `load <file>`, `series <n>`, `debug`, `exit`).
- `API.py` — FastAPI web server exposing `POST /calculate` and `GET /history` endpoints.
- `TestCalculatorAndFraction.py` & `TestAPI.py` — `unittest` test suites covering core classes, edge cases, file operations, and HTTP endpoints.

## Installation & Usage

1. **Install dependencies:** The project uses `multipledispatch`, `fastapi`, `pydantic`, `uvicorn`, and `httpx` (for FastAPI `TestClient`).
```bash
pip install multipledispatch fastapi pydantic uvicorn httpx
```
2. **Run the CLI:**
```bash
python CLI.py
```
3. **Run the FastAPI server:**
```bash
uvicorn API:app --reload
```
4. **Run unit tests:**
```bash
python -m unittest TestCalculatorAndFraction.py TestAPI.py
```
