"""Verifica, en copias temporales, que las pruebas detectan un error por función."""

from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
MUTATIONS = [
    ("square", "TestSquare", "return n * n", "return n + n"),
    ("factorial", "TestFactorial", "return result", "return result + 1"),
    ("is_prime", "TestIsPrime", "if n < 4:\n        return True",
     "if n < 4:\n        return False"),
    ("gcd", "TestGcd", "    return a\n", "    return 1\n"),
    ("lcm", "TestLcm", "return abs(a * b) // gcd(a, b)", "return abs(a * b)"),
]


def main():
    baseline = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=ROOT)
    if baseline.returncode:
        return baseline.returncode

    detected = 0
    for name, test_class, before, after in MUTATIONS:
        with TemporaryDirectory(prefix=f"adminsp7-{name}-") as temporary:
            target = Path(temporary)
            for folder in ("mathlib", "tests"):
                shutil.copytree(
                    ROOT / folder, target / folder,
                    ignore=shutil.ignore_patterns("__pycache__"),
                )
            source = target / "mathlib" / "basic.py"
            content = source.read_text(encoding="utf-8")
            if content.count(before) != 1:
                raise RuntimeError(f"No se encontró la implementación esperada de {name}")
            source.write_text(content.replace(before, after, 1), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", f"tests/test_basic.py::{test_class}"],
                cwd=target, capture_output=True, text=True, encoding="utf-8",
                errors="replace",
            )
            # pytest: 1 significa pruebas fallidas; errores de colección no cuentan.
            if result.returncode == 1 and "AssertionError" in result.stdout:
                detected += 1
                print(f"DETECTADO: {name} - {result.stdout.strip().splitlines()[-1]}", flush=True)
            else:
                print(f"ERROR: mutación de {name} no validada", flush=True)
                print(result.stdout, result.stderr)
    print(f"\nMutaciones detectadas: {detected}/{len(MUTATIONS)}")
    return 0 if detected == len(MUTATIONS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
