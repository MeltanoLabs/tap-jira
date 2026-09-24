"""Tests for IssueComments behavior."""

from __future__ import annotations

from tap_jira.streams import IssueComments
from tap_jira.tap import TapJira

BASE_CONFIG = {
    "domain": "test.atlassian.net",
    "email": "test@example.com",
    "api_token": "test-token",
}


def test_get_url_params_expand_not_set() -> None:
    tap = TapJira(config=BASE_CONFIG)

    stream = IssueComments(tap)
    params = stream.get_url_params(context=None, next_page_token=None)

    assert "expand" not in params


def test_get_url_params_expand() -> None:
    tap = TapJira(
        config={
            **BASE_CONFIG,
            "stream_options": {"issue_comments": {"expand": "renderedBody"}},
        },
    )

    stream = IssueComments(tap)
    params = stream.get_url_params(context=None, next_page_token=None)

    assert params["expand"] == "renderedBody"
