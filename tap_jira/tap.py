#tap_jira/tap.py
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
            "auth_type",
            th.StringType,
            description="Authentication type ('basic' or 'oauth2')",
            default="basic"
        ),
        # Basic Auth Settings
        th.Property(
            "api_token",
            th.StringType,
            description="Jira API Token (required for basic auth)",
            secret=True,
            required=False,
        ),
        th.Property(
            "email",
            th.StringType,
            description="The user email for your Jira account (required for basic auth)",
            required=False,
        ),
        # OAuth2 Settings
        th.Property(
            "client_id",
            th.StringType,
            description="OAuth2 Client ID (required for OAuth)",
            required=False,
        ),
        th.Property(
            "client_secret",
            th.StringType,
            description="OAuth2 Client Secret (required for OAuth)",
            secret=True,
            required=False,
        ),
        th.Property(
            "access_token",
            th.StringType,
            description="OAuth2 Access Token",
            secret=True,
            required=False,
        ),
        th.Property(
            "refresh_token",
            th.StringType,
            description="OAuth2 Refresh Token",
            secret=True,
            required=False,
        ),
        # Common Settings
        th.Property(
            "domain",
            th.StringType,
            description="The Domain for your Jira account, e.g. meltano.atlassian.net",
            required=True,
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest record date to sync",
        ),
        th.Property(
            "end_date",
            th.DateTimeType,
            description="Latest record date to sync",
        ),
        th.Property(
            "page_size",
            th.ObjectType(
                th.Property(
                    "issues",
                    th.IntegerType,
                    description="Page size for issues stream",
                    default=100,
                ),
            ),
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
            streams.WorkflowStatusStream(self),
            streams.IssueStream(self),
            streams.PermissionStream(self),
            streams.ProjectRoleStream(self),
            streams.PriorityStream(self),
            streams.PermissionHolderStream(self),
            streams.SprintStream(self),
            streams.ProjectRoleActorStream(self),
            streams.AuditingStream(self),
            streams.DashboardStream(self),
            streams.FilterSearchStream(self),
            streams.FilterDefaultShareScopeStream(self),
            streams.GroupsPickerStream(self),
            streams.LicenseStream(self),
            streams.ScreensStream(self),
            streams.ScreenSchemesStream(self),
            streams.StatusesSearchStream(self),
            streams.WorkflowStream(self),
            streams.WorkflowSearchStream(self),
            streams.Resolutions(self),
            streams.IssueChangeLogStream(self),
            streams.IssueComments(self),
            streams.BoardStream(self),
            streams.IssueWatchersStream(self),
            streams.IssueWorklogs(self),
        ]


if __name__ == "__main__":
    TapJira.cli()
