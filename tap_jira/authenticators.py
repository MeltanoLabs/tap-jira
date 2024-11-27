#tap_jira/authenticators.py
"""Authentication handling for tap-jira."""

from datetime import datetime, timedelta, timezone
from typing import Optional

import requests
from singer_sdk.authenticators import APIAuthenticatorBase, BasicAuthenticator


class JiraAuthError(Exception):
    """Custom exception for Jira authentication errors."""
    pass


class JiraOAuthError(JiraAuthError):
    """Custom exception for OAuth-related errors."""
    pass


class JiraBasicAuthenticator(BasicAuthenticator):
    """Handles Basic authentication for Jira using API tokens."""

    def __init__(self, stream) -> None:
        """Initialize authenticator.
        
        Args:
            stream: The stream instance requiring authentication.
            
        Raises:
            JiraAuthError: If email or api_token is missing.
        """
        email = stream.config.get("email")
        api_token = stream.config.get("api_token")
        
        if not email or not api_token:
            raise JiraAuthError(
                "Both email and api_token are required for basic authentication"
            )
            
        super().__init__(
            stream=stream,
            username=email,
            password=api_token,
        )

class JiraOAuth2Authenticator(APIAuthenticatorBase):
    """Handles OAuth 2.0 authentication for Jira."""

    def __init__(
        self,
        stream,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
    ) -> None:
        """Initialize authenticator.
        
        Args:
            stream: The stream instance requiring authentication.
            client_id: OAuth2 client ID.
            client_secret: OAuth2 client secret.
            access_token: OAuth2 access token.
            refresh_token: OAuth2 refresh token.
        """
        super().__init__(stream=stream)
        self.client_id = client_id or stream.config.get("client_id")
        self.client_secret = client_secret or stream.config.get("client_secret")
        self._access_token = access_token or stream.config.get("access_token")
        self._refresh_token = refresh_token or stream.config.get("refresh_token")
        self._expires_at: Optional[datetime] = None

        if not self._access_token:
            raise JiraOAuthError(
                "access_token is required for OAuth authentication"
            )

    def get_auth_header(self) -> dict:
        """Return a dictionary of OAuth headers.
        
        Returns:
            Dictionary containing the Authorization header.
        """
        return {"Authorization": f"Bearer {self._access_token}"}

    @property
    def auth_headers(self) -> dict:
        """Return headers with valid OAuth token.
        
        Returns:
            Dictionary containing authentication headers.
        """
        if self.is_token_expired():
            self.refresh_access_token()
        return self.get_auth_header()

    def is_token_expired(self) -> bool:
        """Check if token is expired.
        
        Returns:
            True if token is expired, False otherwise.
        """
        if not self._expires_at:
            return False
        return datetime.now(timezone.utc) >= self._expires_at

    def refresh_access_token(self) -> None:
        """Refresh OAuth access token.
        
        Raises:
            JiraOAuthError: If required OAuth credentials are missing or refresh fails.
        """
        if not (self.client_id and self.client_secret and self._refresh_token):
            raise JiraOAuthError(
                "Missing OAuth2 credentials for refresh. Ensure client_id, client_secret, "
                "and refresh_token are provided."
            )

        try:
            response = requests.post(
                "https://auth.atlassian.com/oauth/token",
                json={
                    "grant_type": "refresh_token",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": self._refresh_token,
                },
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            raise JiraOAuthError(f"Failed to refresh access token: {str(e)}") from e
            
        self._access_token = data["access_token"]
        if "refresh_token" in data:
            self._refresh_token = data["refresh_token"]
        self._expires_at = datetime.now(timezone.utc) + timedelta(seconds=data["expires_in"])


class JiraAuthenticator:
    """Factory class for creating appropriate Jira authenticator."""

    @staticmethod
    def create_for_stream(stream) -> APIAuthenticatorBase:
        """Create and return an authenticator instance for the stream.
        
        Args:
            stream: The stream instance requiring authentication.
            
        Returns:
            An authenticator instance appropriate for the stream's configuration.
            
        Raises:
            JiraAuthError: If authentication configuration is invalid.
        """
        auth_type = stream.config.get("auth_type", "basic")

        if auth_type == "oauth2":
            return JiraOAuth2Authenticator(stream=stream)
        elif auth_type == "basic":
            return JiraBasicAuthenticator(stream=stream)
        else:
            raise JiraAuthError(f"Unsupported authentication type: {auth_type}")