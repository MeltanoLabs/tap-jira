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
            description="Earliest record date to sync",
        ),
        th.Property(
            "end_date",
            th.DateTimeType,
            description="Latest record date to sync",
        ),
        th.Property(
            "domain",
            th.StringType,
            description="Site URL",
            required=True,
        ),
        th.Property(
            "auth",
            th.DiscriminatedUnion(
                "flow",
                oauth=th.ObjectType(
                    th.Property(
                        "access_token", th.StringType, required=True, secret=True
                    ),
                    additional_properties=False,
                ),
                password=th.ObjectType(
                    th.Property("username", th.StringType, required=True),
                    th.Property("password", th.StringType, required=True, secret=True),
                    additional_properties=False,
                ),
            ),
            required=True,
        ),
        th.Property(
            "page_size",
            th.ObjectType(
                th.Property("issues", th.IntegerType, description="Page size for issues stream", default=100),
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
