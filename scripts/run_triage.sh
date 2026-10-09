#!/usr/bin/env bash
# Safe wrapper around main.py.
# Runs a free pass first, asks before spending API credits,
# and saves each report with a timestamp.
# Usage: ./run_triage.sh [path/to/tests]

set -euo pipefail
cd "$(dirname "$0")/.."

TESTS="${1:-seeded_suite/test_suite.py}"
REPORT_DIR="reports"
STAMP=$(date +%Y%m%d_%H%M%S)
OUT="$REPORT_DIR/report_$STAMP.md"

mkdir -p "$REPORT_DIR"

echo "Step 1: free pass (no API calls) on $TESTS"
SUMMARY=$(python3 main.py --tests "$TESTS" --no-triage --out "$OUT" | grep "passed")
echo "$SUMMARY"

FAILED=$(echo "$SUMMARY" | grep -o '[0-9]* failed' | grep -o '[0-9]*')

if [ "$FAILED" -eq 0 ]; then
  echo "No failures, nothing to triage."
  exit 0
fi

read -r -p "Send $FAILED failures to Claude? This uses API credits. (y/n) " ANSWER
if [ "$ANSWER" != "y" ]; then
  echo "Skipped. Free report saved to $OUT"
  exit 0
fi

if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo "ANTHROPIC_API_KEY is not set. Run: export ANTHROPIC_API_KEY=your-key"
  exit 1
fi

echo "Step 2: triaging with Claude"
python3 main.py --tests "$TESTS" --out "$OUT" > /dev/null
echo "Triaged report saved to $OUT"