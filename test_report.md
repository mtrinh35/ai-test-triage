# Test Run Report
_Generated 2026-08-11 19:43:11_

## Summary
- Total tests: **10**
- Passed: **8**
- Failed: **2**
- Duration: **0.02s**

## Failed Tests (sorted by priority)

| Test | Priority | Category | Root Cause | Suggested Fix |
|---|---|---|---|---|
| `sample_tests/test_calculator.py::test_divide_by_zero` | high | logic_bug | The divide function lacks a guard clause for b == 0, causing an unhandled ZeroDivisionError instead of returning a defined value. | Add a check in divide() to handle b == 0 (e.g., return 0, raise a custom exception, or return None) based on intended behavior, and update the test to assert that behavior. |
| `sample_tests/test_calculator.py::test_average_basic` | high | logic_bug | The average() function has an off-by-one error causing it to miscalculate the mean, returning 6.0 instead of 4 for input [2, 4, 6]. | Review the average() implementation, likely a division by incorrect length (e.g., dividing by 1 instead of len(list)), and correct the calculation logic. |