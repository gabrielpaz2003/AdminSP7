"""Operaciones matemáticas básicas con validación explícita de argumentos."""


def _require_number(value, name="n"):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} debe ser un número, se recibió {type(value).__name__}")


def _require_int(value, name="n"):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} debe ser un entero, se recibió {type(value).__name__}")


def square(n):
    """Retorna n² para int o float; rechaza bool y otros tipos con TypeError."""
    _require_number(n)
    return n + n  # Error intencional para demostrar el bloqueo del PR.


def factorial(n):
    """Retorna n! para enteros n >= 0; 0! = 1; negativos causan ValueError."""
    _require_int(n)
    if n < 0:
        raise ValueError("factorial no está definido para números negativos")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def is_prime(n):
    """Indica si un entero es primo; los enteros menores que 2 no lo son."""
    _require_int(n)
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def gcd(a, b):
    """Calcula el MCD no negativo de dos enteros; (0, 0) causa ValueError."""
    _require_int(a, "a")
    _require_int(b, "b")
    if a == 0 and b == 0:
        raise ValueError("gcd(0, 0) no está definido")
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Calcula el MCM positivo; por contrato, rechaza ceros con ValueError."""
    _require_int(a, "a")
    _require_int(b, "b")
    if a == 0 or b == 0:
        raise ValueError("lcm no está definido cuando algún argumento es 0")
    return abs(a * b) // gcd(a, b)
