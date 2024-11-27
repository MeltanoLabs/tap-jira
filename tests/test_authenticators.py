from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch

import pytest
from tap_jira.authenticators import JiraOAuth2Authenticator, JiraOAuthError

class TestJiraOAuth2Authenticator:
    def test_init_with_valid_credentials(self):
        stream = Mock(
            config={
                "client_id": "client_id",
                "client_secret": "client_secret",
                "access_token": "access_token",
                "refresh_token": "refresh_token",
            }
        )
        authenticator = JiraOAuth2Authenticator(stream)
        assert authenticator.client_id == "client_id"
        assert authenticator.client_secret == "client_secret"
        assert authenticator._access_token == "access_token"
        assert authenticator._refresh_token == "refresh_token"

    def test_init_with_missing_access_token(self):
        stream = Mock(config={"access_token": None})
        with pytest.raises(JiraOAuthError):
            JiraOAuth2Authenticator(stream)

    @patch("tap_jira.authenticators.requests.post")
    def test_refresh_access_token(self, mock_post):
        mock_post.return_value.json.return_value = {
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 3600,
        }
        stream = Mock(
            config={
                "client_id": "client_id",
                "client_secret": "client_secret",
                "refresh_token": "refresh_token",
            }
        )
        authenticator = JiraOAuth2Authenticator(
            stream, access_token="existing_access_token"
        )
        authenticator.refresh_access_token()
        assert authenticator._access_token == "new_access_token"
        assert authenticator._refresh_token == "new_refresh_token"
        assert authenticator._expires_at > datetime.now(timezone.utc)

    @patch("tap_jira.authenticators.requests.post")
    def test_refresh_access_token_with_missing_credentials(self, mock_post):
        stream = Mock(config={"client_id": None, "client_secret": None, "refresh_token": None})
        authenticator = JiraOAuth2Authenticator(stream, access_token="existing_access_token")
        with pytest.raises(JiraOAuthError):
            authenticator.refresh_access_token()