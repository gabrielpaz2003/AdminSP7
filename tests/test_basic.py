import pytest

from mathlib import square, factorial, is_prime, gcd, lcm


class TestSquare:
    def test_positive_integer(self):
        assert square(4) == 16

    def test_negative_integer(self):
        assert square(-3) == 9

    def test_float(self):
        assert square(1.5) == pytest.approx(2.25)

    def test_zero(self):
        assert square(0) == 0

    @pytest.mark.parametrize("bad", ["4", None, [2], True, False])
    def test_invalid_type_raises(self, bad):
        with pytest.raises(TypeError):
            square(bad)


class TestFactorial:
    def test_small_number(self):
        assert factorial(5) == 120

    def test_larger_number(self):
        assert factorial(10) == 3628800

    @pytest.mark.parametrize("n", [0, 1])
    def test_zero_and_one(self, n):
        assert factorial(n) == 1

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            factorial(-1)

    @pytest.mark.parametrize("bad", [2.5, "5", None, True, False])
    def test_invalid_type_raises(self, bad):
        with pytest.raises(TypeError):
            factorial(bad)


class TestIsPrime:
    @pytest.mark.parametrize("n", [2, 3, 5, 13, 97, 7919])
    def test_primes(self, n):
        assert is_prime(n) is True

    @pytest.mark.parametrize("n", [4, 9, 15, 25, 100, 7917])
    def test_composites(self, n):
        assert is_prime(n) is False

    @pytest.mark.parametrize("n", [1, 0, -7])
    def test_less_than_two_is_not_prime(self, n):
        assert is_prime(n) is False

    @pytest.mark.parametrize("bad", [7.0, "7", None, True, False])
    def test_invalid_type_raises(self, bad):
        with pytest.raises(TypeError):
            is_prime(bad)


class TestGcd:
    def test_common_divisor(self):
        assert gcd(12, 18) == 6

    def test_coprime(self):
        assert gcd(17, 5) == 1

    @pytest.mark.parametrize("a, b", [(0, 9), (9, 0), (0, -9), (-9, 0)])
    def test_with_zero(self, a, b):
        assert gcd(a, b) == 9

    @pytest.mark.parametrize("a, b", [(-12, 18), (12, -18), (-12, -18)])
    def test_negative_numbers(self, a, b):
        assert gcd(a, b) == 6

    def test_both_zero_raises(self):
        with pytest.raises(ValueError):
            gcd(0, 0)

    @pytest.mark.parametrize("bad", [12.0, "12", None, True, False])
    @pytest.mark.parametrize("position", [0, 1])
    def test_invalid_type_raises(self, bad, position):
        args = [12, 18]
        args[position] = bad
        with pytest.raises(TypeError):
            gcd(*args)


class TestLcm:
    def test_common_multiple(self):
        assert lcm(4, 6) == 12

    def test_coprime(self):
        assert lcm(7, 5) == 35

    @pytest.mark.parametrize("a, b", [(-4, 6), (4, -6), (-4, -6)])
    def test_negative_numbers(self, a, b):
        assert lcm(a, b) == 12

    @pytest.mark.parametrize("a, b", [(0, 5), (5, 0), (0, 0)])
    def test_zero_raises(self, a, b):
        with pytest.raises(ValueError):
            lcm(a, b)

    @pytest.mark.parametrize("bad", [4.0, "4", None, True, False])
    @pytest.mark.parametrize("position", [0, 1])
    def test_invalid_type_raises(self, bad, position):
        args = [4, 6]
        args[position] = bad
        with pytest.raises(TypeError):
            lcm(*args)
