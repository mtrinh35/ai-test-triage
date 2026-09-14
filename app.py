"""
Small module with intentionally seeded bugs and behaviors.
Used to generate a realistic mix of test failures for the AI Test Triage Agent.
"""

import time
import random


# ---- CORRECTNESS BUGS ----

def add_tax(price, tax_rate):
    """Bug: tax_rate should be a percentage (e.g. 0.08), but this treats it as already-scaled."""
    return price + tax_rate  # should be price + (price * tax_rate)


def find_max(numbers):
    """Bug: off-by-one, ignores the last element."""
    current_max = numbers[0]
    for i in range(len(numbers) - 1):  # should be range(len(numbers))
        if numbers[i] > current_max:
            current_max = numbers[i]
    return current_max


# ---- EDGE CASE BUGS ----

def calculate_average(values):
    """Bug: crashes on empty list instead of handling it."""
    return sum(values) / len(values)


def get_first_char(s):
    """Bug: crashes on empty string."""
    return s[0]


# ---- EXCEPTION / MALFORMED INPUT BUGS ----

def parse_config(data: dict):
    """Bug: assumes 'timeout' key always exists."""
    return {
        "name": data["name"],
        "timeout": data["timeout"],  # KeyError if missing
    }


# ---- PERFORMANCE / TIMEOUT ISSUE ----

def has_duplicate(items):
    """Intentionally O(n^2) — slow enough to look like a timeout on large input."""
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                return True
    return False


# ---- FLAKY BEHAVIOR ----

def flaky_network_call():
    """Simulates an intermittent network failure ~30% of the time."""
    if random.random() < 0.3:
        raise ConnectionError("Simulated transient network failure")
    return {"status": "ok"}


# ---- ENVIRONMENT / DEPENDENCY ISSUE ----

def get_db_record(record_id, connection=None):
    """Bug: requires a real connection object; fails if not injected/mocked."""
    if connection is None:
        raise RuntimeError("No database connection configured")
    return connection.fetch(record_id)


# ---- CORRECT / PASSING FUNCTION (control group) ----

def is_even(n):
    return n % 2 == 0
