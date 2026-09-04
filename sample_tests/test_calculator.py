import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from calculator_utils import add, subtract, divide, average, is_even, factorial


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(10, 4) == 6


def test_divide_normal():
    assert divide(10, 2) == 5


def test_divide_by_zero():
    # This will fail with ZeroDivisionError - exposes the missing guard clause
    assert divide(5, 0) == 0


def test_average_basic():
    # This will fail due to the off-by-one bug in average()
    assert average([2, 4, 6]) == 4


def test_is_even_true():
    assert is_even(4) is True


def test_is_even_false():
    assert is_even(7) is False


def test_factorial_base_case():
    assert factorial(0) == 1


def test_factorial_positive():
    assert factorial(5) == 120


def test_factorial_negative_raises():
    try:
        factorial(-3)
        assert False, "expected ValueError"
    except ValueError:
        pass
