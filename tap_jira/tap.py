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
            description="The Domain for your Jira account, e.g. meltano.atlassian.net",
            required=True,
        ),
        th.Property(
            "api_token",
            th.StringType,
            description="Jira API Token.",
            required=True,
            secret=True,
            title="API Token",
        ),
        th.Property(
            "email",
            th.StringType,
            description="The user email for your Jira account.",
            required=True,
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
        th.Property(
            "stream_options",
            th.ObjectType(
                th.Property(
                    "issues",
                    th.ObjectType(
                        th.Property(
                            "jql",
                            th.StringType,
                            description="A JQL query to filter issues",
                            title="JQL Query",
                        ),
                    ),
                    title="Issues Stream Options",
                    description="Options specific to the issues stream",
                ),
            ),
            description="Options for individual streams",
        ),
        th.Property(
            "include_audit_logs",
            th.BooleanType,
            description="Include the audit logs stream",
            default=False,
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.JiraStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        stream_list = [
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

        if self.config.get("include_audit_logs", False):
            stream_list.append(streams.AuditingStream(self))

        return stream_list
