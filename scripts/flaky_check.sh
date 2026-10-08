#!/usr/bin/env bash
# Runs a test file several times and reports how often each test fails.
# A test that fails every run is a real bug. A test that fails only
# some runs are flaky.
# Usage: ./flaky_check.sh [runs] [path/to/tests]

cd "$(dirname "$0")/.."

RUNS="${1:-10}"
TESTS="${2:-seeded_suite/test_suite.py}"
TMP=$(mktemp)

echo "Running $TESTS $RUNS times..."

for i in $(seq 1 "$RUNS"); do
  echo "  run $i of $RUNS"
  python3 -m pytest "$TESTS" -q --tb=no | grep '^FAILED' | sed 's/ - .*//' >> "$TMP"
done

echo
echo "Failures out of $RUNS runs:"

sort "$TMP" | uniq -c | sort -rn | while read -r COUNT NAME; do
  if [ "$COUNT" -eq "$RUNS" ]; then
    LABEL="always fails, real bug"
  else
    LABEL="intermittent, flaky"
  fi
  echo "$COUNT/$RUNS  $NAME  [$LABEL]"
done

rm -f "$TMP"