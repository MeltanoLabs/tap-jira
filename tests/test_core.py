"""Tests standard tap features using the built-in SDK tests library."""

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_jira.tap import TapJira

# Run standard built-in tap tests from the SDK:
TestTapJira = get_tap_test_class(TapJira, suite_config=SuiteConfig())
