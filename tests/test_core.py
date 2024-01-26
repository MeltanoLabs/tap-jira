"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import os

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_jira.tap import TapJira

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
