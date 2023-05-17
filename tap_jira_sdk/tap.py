"""tap-jira-sdk tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_jira_sdk import streams


class Taptap-jira-sdk(Tap):
    """tap-jira-sdk tap class."""

    name = "tap-jira-sdk"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "project_ids",
            th.ArrayType(th.StringType),
            required=True,
            description="Project IDs to replicate",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
        th.Property(
            "api_version",
            th.StringType,
            description="The Jira API version",
        ),
        th.Property(
            "domain",
            th.StringType,
            description="The domain name for the API service",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.tap-jira-sdkStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.UsersStream(self),
            streams.FieldStream(self),
        ]


if __name__ == "__main__":
    Taptap-jira-sdk.cli()
