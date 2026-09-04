"""
main.py - AI Test Triage Agent

Orchestrates: run tests -> extract structured results -> triage failures
with Claude -> generate a markdown report.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python main.py
    python main.py --tests sample_tests --out test_report.md
    python main.py --no-triage      # run/report without calling the API
"""

import argparse
from test_runner import run_tests, extract_results, summarize
from report_generator import generate_report


def main():
    parser = argparse.ArgumentParser(description="AI-assisted test triage pipeline")
    parser.add_argument("--tests", default="sample_tests", help="Path to test directory")
    parser.add_argument("--out", default="test_report.md", help="Output report path")
    parser.add_argument("--no-triage", action="store_true", help="Skip Claude triage (just run + report)")
    args = parser.parse_args()

    print(f"Running tests in '{args.tests}'...")
    raw = run_tests(test_path=args.tests)
    results = extract_results(raw)
    summary = summarize(raw)
    print(f"  {summary['passed']} passed, {summary['failed']} failed, {summary['duration']:.2f}s")

    if not args.no_triage and summary["failed"] > 0:
        from triage_agent import triage_all_failures
        print("Sending failures to Claude for triage...")
        results = triage_all_failures(results)

    report = generate_report(summary, results, output_path=args.out)
    print(f"\nReport written to {args.out}\n")
    print(report)


if __name__ == "__main__":
    main()
