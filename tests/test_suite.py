"""
Seeded test suite for the AI Test Triage Agent.

Categories covered:
  1. Correctness failures
  2. Edge cases
  3. Exception / malformed input
  4. Timeout / performance
  5. Flaky tests
  6. Environment / dependency failures
  7. Batch of simultaneous failures (mixed)

Run with: pytest tests/test_suite.py -v
"""

import sys
import os
import time
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app import (
    add_tax,
    find_max,
    calculate_average,
    get_first_char,
    parse_config,
    has_duplicate,
    flaky_network_call,
    get_db_record,
    is_even,
)


# ---------------------------------------------------------------------------
# 1. CORRECTNESS FAILURES
# ---------------------------------------------------------------------------

def test_add_tax_applies_percentage():
    # Fails: add_tax treats tax_rate as flat amount, not percentage
    assert add_tax(100, 0.08) == 108.0


def test_find_max_includes_last_element():
    # Fails: off-by-one bug skips the last element
    assert find_max([1, 5, 9, 42]) == 42


def test_is_even_control_passes():
    # Passes: control group, should not appear in triage report
    assert is_even(4) is True


# ---------------------------------------------------------------------------
# 2. EDGE CASES
# ---------------------------------------------------------------------------

def test_calculate_average_empty_list():
    # Fails: ZeroDivisionError on empty input
    assert calculate_average([]) == 0


def test_get_first_char_empty_string():
    # Fails: IndexError on empty string
    assert get_first_char("") == ""


def test_calculate_average_normal_case():
    # Passes: sanity check for the happy path
    assert calculate_average([2, 4, 6]) == 4


# ---------------------------------------------------------------------------
# 3. EXCEPTION / MALFORMED INPUT
# ---------------------------------------------------------------------------

def test_parse_config_missing_timeout_key():
    # Fails: KeyError, config missing a required field
    result = parse_config({"name": "service-a"})
    assert result["timeout"] == 30


def test_parse_config_valid_input():
    # Passes: valid input path
    result = parse_config({"name": "service-b", "timeout": 30})
    assert result["name"] == "service-b"


# ---------------------------------------------------------------------------
# 4. TIMEOUT / PERFORMANCE
# ---------------------------------------------------------------------------

@pytest.mark.timeout(2)
def test_has_duplicate_large_input_within_time_limit():
    # Fails/times out: O(n^2) implementation is too slow at this size
    large_list = list(range(20000)) + [19999]
    assert has_duplicate(large_list) is True


def test_has_duplicate_small_input():
    # Passes: small input is fast regardless of algorithm complexity
    assert has_duplicate([1, 2, 3, 4]) is False


# ---------------------------------------------------------------------------
# 5. FLAKY TESTS
# ---------------------------------------------------------------------------

def test_flaky_network_call():
    # Intermittently fails (~30% of runs) due to simulated transient error
    result = flaky_network_call()
    assert result["status"] == "ok"


# ---------------------------------------------------------------------------
# 6. ENVIRONMENT / DEPENDENCY FAILURES
# ---------------------------------------------------------------------------

def test_get_db_record_without_connection():
    # Fails: no connection injected, simulates a missing/misconfigured dependency
    get_db_record(record_id=1)


class FakeConnection:
    def fetch(self, record_id):
        return {"id": record_id, "name": "test-record"}


def test_get_db_record_with_mocked_connection():
    # Passes: dependency correctly mocked
    conn = FakeConnection()
    result = get_db_record(record_id=1, connection=conn)
    assert result["id"] == 1


# ---------------------------------------------------------------------------
# 7. BATCH OF SIMULTANEOUS MIXED FAILURES
#    (run together to test whether triage priority ranking is sensible)
# ---------------------------------------------------------------------------

def test_batch_correctness_bug():
    assert add_tax(50, 0.10) == 55.0


def test_batch_edge_case_bug():
    assert calculate_average([]) == 0


def test_batch_exception_bug():
    parse_config({"name": "batch-service"})


def test_batch_environment_bug():
    get_db_record(record_id=99)
