"""Tap for tap-jira."""

import sys

if sys.version_info < (3, 11):
    from backports.datetime_fromisoformat import (  # ty: ignore[unresolved-import]
        MonkeyPatch,
    )

    MonkeyPatch.patch_fromisoformat()
