"""tap-jira tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_jira import streams


class TapJira(Tap):
    """tap-jira tap class."""

    name = "tap-jira"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
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
        th.Property(
            "account_id",
            th.StringType,
            description="The Jira API accound id",
        ),
        th.Property(
            "board_id",
            th.StringType,
            description="The Jira API board id",
        ),
        th.Property(
            "project_id",
            th.StringType,
            description="The Jira API project id",
        ),
        th.Property(
            "role_admin_id",
            th.StringType,
            description="The Jira API role admin id",
        ),
        th.Property(
            "role_viewer_id",
            th.StringType,
            description="The Jira API role admin id",
        ),
        th.Property(
            "role_member_id",
            th.StringType,
            description="The Jira API role admin id",
        ),
        th.Property(
            "role_altasian_id",
            th.StringType,
            description="The Jira API role admin id",
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
            streams.PermissionHolderStream(self),
            streams.SprintStream(self),
            streams.UserGroupTrustedStream(self),
            streams.ProjectRoleAtlassianActorStream(self),
            streams.IssueWatcherStream(self),
        ]


if __name__ == "__main__":
    TapJira.cli()
