import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import pytest
from unittest.mock import patch
from types import SimpleNamespace
from triage_agent import triage_failure, triage_all_failures


def make_fake_client(response_text):
    """Builds a fake Anthropic client that returns a fixed response."""
    fake_block = SimpleNamespace(type="text", text=response_text)
    fake_response = SimpleNamespace(content=[fake_block])

    class FakeMessages:
        def create(self, **kwargs):
            return fake_response

    class FakeClient:
        messages = FakeMessages()

    return FakeClient()


def test_triage_failure_parses_valid_json():
    fake_json = json.dumps({
        "category": "logic_bug",
        "root_cause": "off-by-one in average calculation",
        "suggested_fix": "remove the -1",
        "priority": "high",
    })
    client = make_fake_client(fake_json)
    test_result = {
        "name": "test_average_basic",
        "error_message": "assert 6.0 == 4",
        "traceback": "...",
    }

    result = triage_failure(client, test_result)

    assert result["category"] == "logic_bug"
    assert result["priority"] == "high"


def test_triage_failure_strips_code_fences():
    fake_json = "```json\n" + json.dumps({
        "category": "flaky_test",
        "root_cause": "timing issue",
        "suggested_fix": "add a retry",
        "priority": "low",
    }) + "\n```"
    client = make_fake_client(fake_json)
    test_result = {"name": "t", "error_message": "e", "traceback": "tb"}

    result = triage_failure(client, test_result)

    assert result["category"] == "flaky_test"


def test_triage_failure_falls_back_on_malformed_json():
    client = make_fake_client("not valid json {{{")
    test_result = {"name": "t", "error_message": "e", "traceback": "tb"}

    result = triage_failure(client, test_result)

    assert result["category"] == "unknown"
    assert result["priority"] == "medium"

def test_triage_all_failures_only_triages_failed_tests(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake-key-for-test")

    fake_json = json.dumps({
        "category": "logic_bug",
        "root_cause": "x",
        "suggested_fix": "y",
        "priority": "high",
    })
    fake_client = make_fake_client(fake_json)

    with patch("triage_agent.Anthropic", return_value=fake_client):
        results = [
            {"name": "test_a", "outcome": "passed", "error_message": None, "traceback": None},
            {"name": "test_b", "outcome": "failed", "error_message": "boom", "traceback": "..."},
        ]

        triaged = triage_all_failures(results)

        assert "triage" not in triaged[0]
        assert triaged[1]["triage"]["category"] == "logic_bug"


def test_triage_all_failures_raises_without_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        triage_all_failures([{"name": "test_a", "outcome": "failed"}])