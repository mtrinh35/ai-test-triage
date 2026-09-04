"""
CalculatorUtils - a small math utility module.

NOTE FOR DEMO: file contains a couple of intentional bugs so the
triage agent has real failures to analyze. 
"""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def divide(a, b):
    # BUG: no guard against b == 0, will raise ZeroDivisionError
    return a / b


def average(numbers):
    # BUG: off-by-one, uses len(numbers) - 1 instead of len(numbers)
    return sum(numbers) / (len(numbers) - 1)


def is_even(n):
    return n % 2 == 0


def factorial(n):
    if n < 0:
        raise ValueError("factorial undefined for negative numbers")
    if n == 0:
        return 1
    return n * factorial(n - 1)
