"""Tests standard tap features using the built-in SDK tests library."""

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_jira.tap import TapJira

# Minimal configuration for testing
SAMPLE_CONFIG = {
    "domain": "test.atlassian.net",
    "email": "test@example.com",
    "api_token": "test-token",
}

# Run standard built-in tap tests from the SDK:
TestTapJira = get_tap_test_class(
    TapJira,
    config=SAMPLE_CONFIG,
    suite_config=SuiteConfig(),
)
