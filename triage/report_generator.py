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
        for r in failed_sorted:
            t = r.get("triage", {})
            priority = t.get("priority", "-").upper()
            category = t.get("category", "-")
            lines.append(f"### `{r['name']}`")
            lines.append(f"**Priority:** {priority}  |  **Category:** {category}\n")
            lines.append(f"**Root cause:** {t.get('root_cause', '-')}\n")
            lines.append(f"**Suggested fix:** {t.get('suggested_fix', '-')}\n")
            lines.append("---\n")

    report_text = "\n".join(lines)
    with open(output_path, "w") as f:
        f.write(report_text)

    return report_text
