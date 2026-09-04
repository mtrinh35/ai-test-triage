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

`calculator_utils.py` + `sample_tests/` contain two intentional bugs
(divide-by-zero, an off-by-one in `average()`) so there's something real
for the agent to triage out of the box. Swap in your own module and tests
once you've seen it work.

## Why this project

Built to demonstrate the overlap between test automation and AI-agent
tooling: running suites, capturing structured failure data, using an LLM to
triage/categorize/prioritize failures automatically, and producing a report
a QA team could act on without reading raw tracebacks.

## Extending it (good next steps for this project)

- **Test scheduling:** use the AI-assigned priority to reorder a test queue
  (run high-priority/likely-broken tests first) - maps to "optimize test
  scheduling."
- **MCP integration:** wrap this as an MCP server so an agent (Claude Code,
  a chat interface, etc.) can trigger test runs and pull triage reports as
  a tool call, instead of running the CLI by hand.
- **Ansible hook:** call this from an Ansible playbook after a test-environment
  provisioning step, so environment setup and test execution are one workflow.
- **CI integration:** run on every push via GitHub Actions; post the report
  as a PR comment instead of a local markdown file.
- **JUnit support:** swap `pytest-json-report` for parsing JUnit XML output
  (`mvn test` produces this) if you want to reuse this against your existing
  Java projects instead of Python ones.
