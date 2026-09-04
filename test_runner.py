"""
test_runner.py

Executes a pytest suite and converts the results into a clean, structured
format (list of dicts) that downstream stages (triage_agent, report_generator)
can consume - decoupled from pytest's own report format.
"""

import json
import subprocess
import sys
from pathlib import Path


def run_tests(test_path="sample_tests", report_path="report.json"):
    """
    Runs pytest with the json-report plugin and returns the raw report dict.
    """
    cmd = [
        sys.executable, "-m", "pytest", test_path,
        "--json-report", f"--json-report-file={report_path}",
        "-q",
    ]
    subprocess.run(cmd, capture_output=True, text=True)

    report_file = Path(report_path)
    if not report_file.exists():
        raise RuntimeError("pytest did not produce a report file - check that pytest-json-report is installed")

    with open(report_file) as f:
        return json.load(f)


def extract_results(raw_report):
    """
    Flattens the pytest-json-report output into a simple list of test results:
    [{name, outcome, duration, error_message, traceback}, ...]
    """
    results = []
    for test in raw_report.get("tests", []):
        entry = {
            "name": test.get("nodeid"),
            "outcome": test.get("outcome"),
            "duration": test.get("duration", 0.0),
            "error_message": None,
            "traceback": None,
        }
        if test.get("outcome") == "failed":
            call = test.get("call", {})
            longrepr = call.get("longrepr", "")
            entry["traceback"] = longrepr
            # last non-empty line is usually the assertion/exception message
            lines = [l for l in str(longrepr).splitlines() if l.strip()]
            entry["error_message"] = lines[-1] if lines else "Unknown failure"
        results.append(entry)
    return results


def summarize(raw_report):
    summary = raw_report.get("summary", {})
    return {
        "total": summary.get("total", 0),
        "passed": summary.get("passed", 0),
        "failed": summary.get("failed", 0),
        "duration": raw_report.get("duration", 0.0),
    }


if __name__ == "__main__":
    raw = run_tests()
    results = extract_results(raw)
    summary = summarize(raw)
    print(json.dumps({"summary": summary, "results": results}, indent=2))
