"""Introduce o corrige un error controlado en square para demostrar el CI."""

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["break", "fix"])
    args = parser.parse_args()
    path = Path(__file__).resolve().parents[1] / "mathlib" / "basic.py"
    correct = "    return n * n\n"
    broken = "    return n + n  # Error intencional para demostrar el bloqueo del PR.\n"
    before, after = (correct, broken) if args.action == "break" else (broken, correct)
    content = path.read_text(encoding="utf-8")
    if content.count(before) != 1:
        parser.error("No se encontró el estado esperado de square; revisa git diff.")
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(content.replace(before, after, 1))
    print("Error introducido." if args.action == "break" else "Función corregida.")
    print("Ejecuta: python -m pytest -q")


if __name__ == "__main__":
    main()
