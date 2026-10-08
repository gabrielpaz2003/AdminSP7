# Práctica 7: Continuous Integration

[![Pruebas unitarias](https://github.com/gabrielpaz2003/AdminSP7/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/gabrielpaz2003/AdminSP7/actions/workflows/tests.yml)

**CC3047 - Administración y Mantenimiento de Sistemas, UVG, ciclo II 2026.**

Implementación de la **opción A: matemática básica**, con Python, pytest, Git y
GitHub Actions. El repositorio conserva el historial del proyecto original
[Its-Japo/AdminSP7](https://github.com/Its-Japo/AdminSP7).

**Enlace de entrega:** https://github.com/gabrielpaz2003/AdminSP7

## Instalación y ejecución

Requiere Python 3.13 (la versión utilizada por el CI) y Git. Solo se necesita
GitHub CLI (`gh`) para ejecutar desde la terminal los pasos de la demostración.

```bash
git clone https://github.com/gabrielpaz2003/AdminSP7.git
cd AdminSP7
python -m venv .venv
```

En Windows PowerShell, sin necesidad de activar el entorno:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
```

En Linux o macOS:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -v
```

Resultado esperado: **77 pruebas aprobadas**. Se fija `pytest==8.3.3` en
`requirements.txt`. No se necesitan servicios externos ni credenciales para
ejecutar la librería o sus pruebas.

## Funciones y casos de prueba

```python
from mathlib import square, factorial, is_prime, gcd, lcm

square(4)       # 16
factorial(5)    # 120
is_prime(13)    # True
gcd(12, 18)    # 6
lcm(4, 6)     # 12
```

| Función | Funcionamiento | Ejemplos exitosos | Bordes y errores |
| --- | --- | --- | --- |
| `square(n)` | Multiplica el número por sí mismo. | `4 → 16`, `-3 → 9`, `1.5 → 2.25` | `0 → 0`; texto, `None`, listas y booleanos causan `TypeError`. |
| `factorial(n)` | Acumula el producto de los enteros de 2 a n. | `5 → 120`, `10 → 3628800` | `0! = 1! = 1`; negativos causan `ValueError`; tipos no enteros causan `TypeError`. |
| `is_prime(n)` | Descarta menores que 2 y pares; busca divisores impares hasta la raíz cuadrada. | `13 → True`, `97 → True`, `25 → False` | `1`, `0` y negativos retornan `False`; tipos no enteros causan `TypeError`. |
| `gcd(a, b)` | Usa el algoritmo de Euclides sobre valores absolutos. | `(12,18) → 6`, `(17,5) → 1` | Acepta un cero y signos negativos; `(0,0)` causa `ValueError`; valida ambos argumentos. |
| `lcm(a, b)` | Calcula `abs(a*b) // gcd(a,b)`. | `(4,6) → 12`, `(7,5) → 35` | Acepta signos negativos; un cero en cualquiera de los argumentos causa `ValueError`; valida ambos tipos. |

El contrato original de esta librería **rechaza los ceros en `lcm`**. Es una
decisión explícita del proyecto: otras librerías definen el MCM con cero como
cero. `bool` se rechaza incluso siendo una subclase de `int` en Python.

Las pruebas usan `assert` para resultados y `pytest.raises` para excepciones.
`pytest.approx` compara el resultado decimal. `pytest.mark.parametrize`
ejecuta cada entrada por separado y permite identificar exactamente cuál falla.

## Comprobar que las pruebas detectan errores

```powershell
.\.venv\Scripts\python.exe scripts/check_mutations.py
```

El script verifica primero las 77 pruebas originales. Después copia la librería
y las pruebas a carpetas temporales e introduce **un error independiente en cada
función**. Cada modificación debe provocar fallos de aserción en sus pruebas.
Resultado esperado: `Mutaciones detectadas: 5/5`. El código del proyecto queda
intacto. En Linux/macOS se usa `.venv/bin/python`.

## Integración continua y protección

El archivo [`.github/workflows/tests.yml`](.github/workflows/tests.yml) ejecuta
las pruebas en cada Pull Request dirigido a `main`, cuando se publica un commit
en `main` y mediante ejecución manual. Instala Python 3.13 y las dependencias,
y ejecuta `python -m pytest -v`. Un fallo devuelve un código distinto de cero
y marca el job **Pruebas unitarias** como fallido.

La protección de `main` exige ese check, exige que la rama esté actualizada,
requiere un Pull Request e incluye a los administradores. No se requieren
aprobaciones adicionales para que una pareja pueda realizar la demostración.
No se permiten force pushes ni eliminación de `main`.

La protección es una configuración de GitHub, no se activa simplemente por
incluir un archivo YAML. Su configuración reproducible está en
[`docs/main-protection.json`](docs/main-protection.json) y puede aplicarla un
administrador del repositorio con:

```bash
gh api --method PUT repos/gabrielpaz2003/AdminSP7/branches/main/protection --input docs/main-protection.json
```

Para auditarla:

```bash
gh api repos/gabrielpaz2003/AdminSP7/branches/main/protection
```

## Demostración y entrega

La [guía de demostración](docs/DEMOSTRACION.md) contiene los comandos y la
explicación para mostrar en clase el **lunes 19 de octubre de 2026**:
un PR con un fallo intencional, el merge bloqueado, la corrección y el merge
habilitado. Las [evidencias](docs/EVIDENCIAS.md) registran las ejecuciones reales.

| Criterio de la rúbrica | Evidencia en el proyecto |
| --- | --- |
| Funciones y manejo de casos esperados/borde (25%) | `mathlib/basic.py`, contratos y validaciones. |
| Git y repositorio público (25%) | Historial conservado, commits descriptivos y ramas de trabajo. |
| Pruebas exitosas, errores y detección de lógica incorrecta (25%) | `tests/test_basic.py`, 77 pruebas y 5 mutaciones detectadas. |
| CI por PR y bloqueo del merge (25%) | Workflow, protección de `main` y PR de demostración. |

La entrega solicitada en Canvas es **el enlace al repositorio público**.
Las evidencias guardadas apoyan la preparación; la evaluación exige también
la demostración en vivo de la pareja.

## Referencias técnicas

- [GitHub: pruebas de Python con Actions](https://docs.github.com/en/actions/tutorials/build-and-test-code/python).
- [GitHub: checks requeridos y bloqueo de merges](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks).
