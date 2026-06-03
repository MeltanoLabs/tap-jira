"""Test Configuration."""

from __future__ import annotations

import os
import sys
import typing as t

if t.TYPE_CHECKING:
    import pathlib

    import pytest


def pytest_report_header(
    config: pytest.Config,  # noqa: ARG001
    start_path: pathlib.Path,  # noqa: ARG001
) -> list[str] | str:
    """Add a header to the test report."""
    tap_jira_vars = [var for var in os.environ if var.startswith("TAP_JIRA")]
    return f"tap-jira environment variables: {tap_jira_vars}"


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest."""
    if sys.version_info < (3, 11):
        config.addinivalue_line(
            "filterwarnings",
            "once:Python 3.10 will reach its end of life on 2026-10:FutureWarning",
        )
