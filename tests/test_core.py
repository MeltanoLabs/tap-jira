"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import os
from unittest.mock import Mock, patch

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_jira.tap import TapJira

from tap_jira.client import JiraStream
from tap_jira.authenticators import JiraBasicAuthenticator, JiraOAuth2Authenticator

SAMPLE_CONFIG = {
    "start_date": "2023-01-01T00:00:00Z",
    "domain": os.environ.get("TAP_JIRA_DOMAIN"),
    "auth": {
        "flow": "password",
            "username": os.environ.get("TAP_JIRA_AUTH_USERNAME"),
            "password": os.environ.get("TAP_JIRA_AUTH_PASSWORD"),
    },
    "page_size": {
        "issues": 100,
    }
}

# Run standard built-in tap tests from the SDK:
TestTapJira = get_tap_test_class(
    TapJira,
    config=SAMPLE_CONFIG,
    suite_config=SuiteConfig(),
)

class TestJiraStream:
    @patch("tap_jira.client.JiraAuthenticator.create_for_stream")
    def test_basic_authenticator(self, mock_create_authenticator):
        mock_create_authenticator.return_value = JiraBasicAuthenticator(MagicMock())
        stream = JiraStream(MagicMock())
        assert isinstance(stream.authenticator, JiraBasicAuthenticator)

    @patch("tap_jira.client.JiraAuthenticator.create_for_stream")
    def test_oauth2_authenticator(self, mock_create_authenticator):
        mock_create_authenticator.return_value = JiraOAuth2Authenticator(MagicMock())
        stream = JiraStream(MagicMock(config={"auth_type": "oauth2"}))
        assert isinstance(stream.authenticator, JiraOAuth2Authenticator)