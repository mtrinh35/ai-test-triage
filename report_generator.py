"""
report_generator.py

Turns the (summary, results) produced by test_runner + triage_agent into
a markdown report suitable for handing to a stakeholder or attaching to
a build pipeline artifact.
"""

from datetime import datetime

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def generate_report(summary, results, output_path="test_report.md"):
    lines = []
    lines.append(f"# Test Run Report")
    lines.append(f"_Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n")

    lines.append("## Summary")
    lines.append(f"- Total tests: **{summary['total']}**")
    lines.append(f"- Passed: **{summary['passed']}**")
    lines.append(f"- Failed: **{summary['failed']}**")
    lines.append(f"- Duration: **{summary['duration']:.2f}s**\n")

    failed = [r for r in results if r["outcome"] == "failed"]

    if not failed:
        lines.append("All tests passed. No triage needed.")
    else:
        # sort by AI-assigned priority so the most urgent issues are at the top
        failed_sorted = sorted(
            failed,
            key=lambda r: PRIORITY_ORDER.get(r.get("triage", {}).get("priority", "medium"), 1),
        )

        lines.append("## Failed Tests (sorted by priority)\n")
        lines.append("| Test | Priority | Category | Root Cause | Suggested Fix |")
        lines.append("|---|---|---|---|---|")
        for r in failed_sorted:
            t = r.get("triage", {})
            lines.append(
                f"| `{r['name']}` "
                f"| {t.get('priority', '-')} "
                f"| {t.get('category', '-')} "
                f"| {t.get('root_cause', '-')} "
                f"| {t.get('suggested_fix', '-')} |"
            )

    report_text = "\n".join(lines)
    with open(output_path, "w") as f:
        f.write(report_text)

    return report_text
