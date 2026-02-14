"""Tests for cloud_id URL construction in tap-jira."""

from __future__ import annotations

import requests.auth

from tap_jira.streams import BoardStream, IssueStream, SprintStream
from tap_jira.tap import TapJira


class TestCloudIdURLConstruction:
    """Test URL construction with cloud_id parameter."""

    def test_platform_api_url_with_cloud_id(self) -> None:
        """Test Platform API URL construction with cloud_id."""
        tap = TapJira(
            config={
                "domain": "test.atlassian.net",
                "email": "test@example.com",
                "api_token": "test-token",
                "cloud_id": "test-cloud-id",
            }
        )
        stream = IssueStream(tap)
        expected_url = "https://api.atlassian.com/ex/jira/test-cloud-id/rest/api/3"
        assert stream.url_base == expected_url

    def test_platform_api_url_without_cloud_id(self) -> None:
        """Test Platform API URL construction without cloud_id (uses domain)."""
        tap = TapJira(
            config={
                "domain": "test.atlassian.net",
                "email": "test@example.com",
                "api_token": "test-token",
            }
        )
        stream = IssueStream(tap)
        expected_url = "https://test.atlassian.net/rest/api/3"
        assert stream.url_base == expected_url

    def test_platform_api_url_no_port_suffix(self) -> None:
        """Test that Platform API URL does not include :443 port suffix."""
        tap = TapJira(
            config={
                "domain": "test.atlassian.net",
                "email": "test@example.com",
                "api_token": "test-token",
            }
        )
        stream = IssueStream(tap)
        assert ":443" not in stream.url_base

    def test_agile_api_url_with_cloud_id(self) -> None:
        """Test Agile API URL construction with cloud_id."""
        tap = TapJira(
            config={
                "domain": "test.atlassian.net",
                "email": "test@example.com",
                "api_token": "test-token",
                "cloud_id": "test-cloud-id",
            }
        )
        board_stream = BoardStream(tap)
        sprint_stream = SprintStream(tap)

        expected_url = "https://api.atlassian.com/ex/jira/test-cloud-id/rest/agile/1.0"
        assert board_stream.url_base == expected_url
        assert sprint_stream.url_base == expected_url

    def test_agile_api_url_without_cloud_id(self) -> None:
        """Test Agile API URL construction without cloud_id (uses domain)."""
        tap = TapJira(
            config={
                "domain": "test.atlassian.net",
                "email": "test@example.com",
                "api_token": "test-token",
            }
        )
        board_stream = BoardStream(tap)
        sprint_stream = SprintStream(tap)

        expected_url = "https://test.atlassian.net/rest/agile/1.0"
        assert board_stream.url_base == expected_url
        assert sprint_stream.url_base == expected_url

    def test_agile_api_url_no_port_suffix(self) -> None:
        """Test that Agile API URL does not include :443 port suffix."""
        tap = TapJira(
            config={
                "domain": "test.atlassian.net",
                "email": "test@example.com",
                "api_token": "test-token",
            }
        )
        board_stream = BoardStream(tap)
        assert ":443" not in board_stream.url_base


class TestBasicAuthentication:
    """Test that Basic Auth is always used regardless of cloud_id."""

    def test_basic_auth_without_cloud_id(self) -> None:
        """Test that Basic Auth is used when cloud_id is not provided."""
        tap = TapJira(
            config={
                "domain": "test.atlassian.net",
                "email": "test@example.com",
                "api_token": "test-token",
            }
        )
        stream = IssueStream(tap)
        authenticator = stream.authenticator

        assert isinstance(authenticator, requests.auth.HTTPBasicAuth)
        assert authenticator.username == "test@example.com"
        assert authenticator.password == "test-token"

    def test_basic_auth_with_cloud_id(self) -> None:
        """Test that Basic Auth is still used when cloud_id is provided."""
        tap = TapJira(
            config={
                "domain": "test.atlassian.net",
                "email": "test@example.com",
                "api_token": "test-token",
                "cloud_id": "test-cloud-id",
            }
        )
        stream = IssueStream(tap)
        authenticator = stream.authenticator

        assert isinstance(authenticator, requests.auth.HTTPBasicAuth)
        assert authenticator.username == "test@example.com"
        assert authenticator.password == "test-token"
