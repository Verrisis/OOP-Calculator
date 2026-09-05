# OOP Terminal Calculator (Fractions & Complex Numbers)

A command-line based calculator built in Python. Originally an Object-Oriented Programming university project, but expanded beyond the core requirements to include complex fraction handling, fault-tolerant file I/O, and strict separation of concerns.

## Key Features

*   **Smart Polymorphism:** No messy `if/else` type-checking ladders. Uses `multipledispatch` to seamlessly calculate mixed expressions (e.g., adding an integer to a complex fraction).
*   **Complex Fractions Support:** A custom `ComplexFraction` class handles equations with real and imaginary parts. It uses a custom RegEx pipeline to parse inputs like `(1/2)+(3/4)i` without heavy string iteration loops.
*   **Fault-Tolerant File I/O:** Can read and calculate equations from text files. If a line is corrupted (e.g., division by zero or bad formatting), the app isolates the error, reports the exact line to the user, and keeps processing the rest of the file.
*   **Encapsulated State:** Operation history and error logs are kept strictly private and returned as immutable tuples to prevent accidental state modification.
*   **Clean Architecture:** The CLI (`ConsoleUI` acting as a Context Manager) is completely decoupled from the math engine (`Calculator`).
*   **REST API Integration:** Expanded the core CLI calculator into a backend microservice using **FastAPI**. It processes JSON payloads, performs calculations via the OOP engine, and returns structured JSON responses with robust HTTP status code handling (400, 404, 501).

## Tech Stack
*   **Language:** Python 3
*   **Architecture:** OOP, Command Pattern (lite), Context Managers
*   **Libraries:** `FastAPI`, `uvicorn`, `multipledispatch`, `re` (Regex), `pytest`

## How to use

**Run the REST API Server:**

```bash
uvicorn api:app --reload​
```

_Once running, navigate to `http://localhost:8000/docs` in your browser to interact with the API via the auto-generated Swagger UI._

**Run the CLI interface:**

```bash
python CLI.py
```

**Supported CLI Commands:**

*   `help` - Shows available commands and usage examples.
*   `history` - Displays a cleanly formatted log of past calculations and caught exceptions.
*   `load <filename>` - Evaluates a list of equations from a `.txt` file (e.g., `load equations.txt`).
*   `clear` - Clears the terminal screen.
*   `exit` (or `quit`) - Safely terminates the application and closes the I/O streams.

## Design Philosophy

The main goal of this project was to stick to SOLID principles. The Open-Closed Principle is maintained via multiple dispatch, and Single Responsibility is enforced by keeping UI logic away from the math pipeline.
