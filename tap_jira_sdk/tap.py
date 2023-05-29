"""tap-jira-sdk tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_jira_sdk import streams


class TapJira(Tap):
    """tap-jira-sdk tap class."""

    name = "tap-jira-sdk"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            #required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the API service",
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
        th.Property(
            "username",
            th.StringType,
            description="The Jira API username",
        ),
        th.Property(
            "password",
            th.StringType,
            description="The Jira API password",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.JiraStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.UsersStream(self),
            streams.FieldStream(self),
            streams.ServerInfoStream(self),
            streams.IssueTypeStream(self),
            streams.ProjectStream(self),
            streams.StatusStream(self),
            streams.IssueStream(self),
            streams.SearchStream(self),
            streams.PermissionStream(self),
            streams.ProjectRoleStream(self),
            streams.PriorityStream(self),
        ]


if __name__ == "__main__":
    TapJira.cli()
