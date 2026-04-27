"""Tests for HTTP headers set on every Jira request."""

from __future__ import annotations

from tap_jira.streams import IssueStream
from tap_jira.tap import TapJira


class TestForceEnglishHeaders:
    """Headers forcing English-language API responses must be present."""

    def test_accept_language_headers_present(self) -> None:
        """Both ``Accept-Language`` and ``X-Force-Accept-Language`` are sent.

        Jira Cloud localizes error messages to the API user's profile
        language. ``X-Force-Accept-Language: true`` together with
        ``Accept-Language: en`` overrides that, keeping ``validate_response``
        string-matching reliable for non-English users.
        """
        tap = TapJira(
            config={
                "domain": "test.atlassian.net",
                "email": "test@example.com",
                "api_token": "test-token",
            },
        )
        headers = IssueStream(tap).http_headers
        assert headers["Accept-Language"] == "en"
        assert headers["X-Force-Accept-Language"] == "true"
