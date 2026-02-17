"""Tests for IssueStream behavior."""

from __future__ import annotations

from tap_jira.streams import IssueStream
from tap_jira.tap import TapJira


def test_get_url_params_jql_start_date():
    tap = TapJira(
        config={
            "domain": "test.atlassian.net",
            "email": "test@example.com",
            "api_token": "test-token",
        },
        state={
            "bookmarks": {
                "issues": {
                    "starting_replication_value": "2026-01-01T12:34:56",
                },
            },
        },
    )

    stream = IssueStream(tap)
    params = stream.get_url_params(context=None, next_page_token=None)

    assert params["jql"] == (
        "(created>='2026-01-01 12:34' or updated>='2026-01-01 12:34') and (id != null) "
        "order by updated asc"
    )


def test_get_url_params_jql_start_and_end_date():
    tap = TapJira(
        config={
            "domain": "test.atlassian.net",
            "email": "test@example.com",
            "api_token": "test-token",
            "end_date": "2026-02-01T00:00:00",
        },
        state={
            "bookmarks": {
                "issues": {
                    "starting_replication_value": "2026-01-01T12:34:56",
                },
            },
        },
    )

    stream = IssueStream(tap)
    params = stream.get_url_params(context=None, next_page_token=None)

    assert params["jql"] == (
        "(created>='2026-01-01 12:34' or updated>='2026-01-01 12:34') and "
        "(created<'2026-02-01 00:00' or updated<'2026-02-01 00:00') and (id != null) "
        "order by updated asc"
    )
