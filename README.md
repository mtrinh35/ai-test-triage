# AI Test Triage Agent

A small pipeline that runs a test suite, sends each failure to Claude for
root-cause triage and prioritization, and generates a stakeholder-ready
markdown report.

**Pipeline:** `test_runner.py` (run + structure results) → `triage_agent.py`
(Claude classifies each failure: category, root cause, fix, priority) →
`report_generator.py` (priority-sorted markdown report) → orchestrated by
`main.py`.

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-your-key-here   # console.anthropic.com
```

## Usage

```bash
python main.py                          # run sample_tests/, triage failures, write test_report.md
python main.py --tests my_tests/        # point at your own test directory
python main.py --no-triage              # just run + report, skip the API calls (no key needed)
```
