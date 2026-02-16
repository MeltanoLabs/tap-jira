"""Tap for tap-jira."""

import sys

if sys.version_info < (3, 11):
    from backports.datetime_fromisoformat import MonkeyPatch  # ty: ignore[unresolved-import]

    MonkeyPatch.patch_fromisoformat()
