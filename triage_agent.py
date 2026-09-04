"""
triage_agent.py

For each failed test, asks Claude to:
  1. Categorize the failure (logic bug / environment / flaky / bad assertion)
  2. Give a one-sentence root-cause explanation
  3. Suggest a concrete fix
  4. Assign a priority (high/medium/low) for triage/scheduling
 
"""

import json
import os
from anthropic import Anthropic

MODEL = "claude-sonnet-5"

TRIAGE_SYSTEM_PROMPT = """You are a test triage assistant for a software QA pipeline.
Given a failing test's name, error message, and traceback, respond with ONLY a JSON
object (no markdown, no preamble) with these exact keys:

{
  "category": one of ["logic_bug", "environment_issue", "flaky_test", "bad_assertion", "unknown"],
  "root_cause": "one clear sentence explaining why this likely failed",
  "suggested_fix": "one or two sentences with a concrete next step",
  "priority": one of ["high", "medium", "low"]
}
"""


def triage_failure(client, test_result):
    """
    Calls Claude to triage a single failed test. Returns a dict with the
    parsed triage fields, or a fallback dict if the call/parse fails.
    """
    user_prompt = (
        f"Test name: {test_result['name']}\n"
        f"Error message: {test_result['error_message']}\n"
        f"Traceback:\n{test_result['traceback']}\n"
    )

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=400,
            system=TRIAGE_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
        text = "".join(block.text for block in response.content if block.type == "text").strip()
        # strip accidental code fences if the model adds them
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        return {
            "category": "unknown",
            "root_cause": f"Triage agent error: {e}",
            "suggested_fix": "Review manually.",
            "priority": "medium",
        }


def triage_all_failures(results):
    """
    Takes the list of test results from test_runner.extract_results(),
    triages every failed one, and attaches the triage info in place.
    Requires ANTHROPIC_API_KEY to be set.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Set the ANTHROPIC_API_KEY environment variable before running triage.")

    client = Anthropic(api_key=api_key)

    for test in results:
        if test["outcome"] == "failed":
            test["triage"] = triage_failure(client, test)

    return results
