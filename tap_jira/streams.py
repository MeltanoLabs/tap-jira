"""Stream type classes for tap-jira."""

from __future__ import annotations

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_jira.client import JiraStream

import requests

PropertiesList = th.PropertiesList
Property = th.Property
ObjectType = th.ObjectType
DateTimeType = th.DateTimeType
StringType = th.StringType
ArrayType = th.ArrayType
BooleanType = th.BooleanType
IntegerType = th.IntegerType
NumberType = th.NumberType
role = {}


class UsersStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-users/#api-rest-api-3-user-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    name = "users"
    path = "/users/search"
    primary_keys = ["accountId"]
    replication_key = "accountId"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[*]"
    instance_name = ""

    schema = PropertiesList(
        Property("self", StringType),
        Property("key", StringType),
        Property("accountId", StringType),
        Property("accountType", StringType),
        Property("emailAddress", StringType),
        Property("name", StringType),
        Property(
            "avatarUrls",
            ObjectType(
                Property("48x48", StringType),
                Property("24x24", StringType),
                Property("16x16", StringType),
                Property("32x32", StringType),
            ),
        ),
        Property("displayName", StringType),
        Property("active", BooleanType),
        Property("timeZone", StringType),
        Property("locale", StringType),
    ).to_dict()

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """

        params: dict = {}
        if next_page_token:
            params["startAt"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def get_next_page_token(
        self,
        response: requests.Response,
        previous_token: t.Any | None,
    ) -> t.Any | None:
        """Return a token for identifying next page or None if no more pages."""
        # If pagination is required, return a token which can be used to get the
        #       next page. If this is the final page, return "None" to end the
        #       pagination loop.
        resp_json = response.json()
        if previous_token is None:
            previous_token = 0

        page = resp_json
        if len(page) == 0:
            return None

        return previous_token + 1


class FieldStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-fields/#api-rest-api-3-field-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "fields"
    path = "/field"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "INCREMENTAL"
    instance_name = ""

    schema = PropertiesList(
        Property("id", StringType),
        Property("key", StringType),
        Property("name", StringType),
        Property("untranslatedName", StringType),
        Property("custom", BooleanType),
        Property("orderable", BooleanType),
        Property("navigable", BooleanType),
        Property("searchable", BooleanType),
        Property("clauseNames", ArrayType(StringType)),
        Property(
            "scope",
            ObjectType(
                Property("type", StringType),
                Property(
                    "project",
                    ObjectType(
                        Property("id", StringType),
                    ),
                ),
            ),
        ),
        Property(
            "schema",
            ObjectType(
                Property("type", StringType),
                Property("system", StringType),
                Property("items", StringType),
                Property("custom", StringType),
                Property("customId", IntegerType),
                Property(
                    "configuration",
                    ObjectType(
                        Property("customRenderer", BooleanType),
                        Property("readOnly", BooleanType),
                        Property("environment", StringType),
                        Property(
                            "com.atlassian.jira.plugin.system.customfieldtypes:atlassian-team",
                            BooleanType,
                        ),
                    ),
                ),
            ),
        ),
    ).to_dict()


class ServerInfoStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-server-info/#api-rest-api-3-serverinfo-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    name = "server_info"
    path = "/serverInfo"
    primary_keys = ["baseUrl"]
    replication_key = "serverTime"
    replication_method = "INCREMENTAL"
    instance_name = ""

    schema = PropertiesList(
        Property("baseUrl", StringType),
        Property("version", StringType),
        Property("versionNumbers", ArrayType(IntegerType)),
        Property("deploymentType", StringType),
        Property("buildNumber", IntegerType),
        Property("buildDate", StringType),
        Property("serverTime", StringType),
        Property("scmInfo", StringType),
        Property("serverTitle", StringType),
        Property(
            "defaultLocale",
            ObjectType(
                Property("locale", StringType),
            ),
        ),
    ).to_dict()


class IssueTypeStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-types/#api-rest-api-3-issuetype-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "issue_types"
    path = "/issuetype"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[*]"  # Or override `parse_response`.
    instance_name = ""

    schema = PropertiesList(
        Property("self", StringType),
        Property("id", StringType),
        Property("description", StringType),
        Property("iconUrl", StringType),
        Property("name", StringType),
        Property("untranslatedName", StringType),
        Property("subtask", BooleanType),
        Property("avatarId", IntegerType),
        Property("hierarchyLevel", IntegerType),
        Property(
            "scope",
            ObjectType(
                Property("type", StringType),
                Property(
                    "project",
                    ObjectType(
                        Property("id", StringType),
                        Property("key", StringType),
                        Property("name", StringType),
                    ),
                ),
            ),
        ),
    ).to_dict()


class WorkflowStatusStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-workflow-statuses/#api-rest-api-3-status-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    name = "workflow_statuses"
    path = "/status"
    primary_keys = ["id"]
    replication_key = "self"
    replication_method = "INCREMENTAL"
    instance_name = ""

    schema = PropertiesList(
        Property("self", StringType),
        Property("description", StringType),
        Property("iconUrl", StringType),
        Property("name", StringType),
        Property("untranslatedName", StringType),
        Property("id", StringType),
        Property(
            "statusCategory",
            ObjectType(
                Property("self", StringType),
                Property("id", IntegerType),
                Property("key", StringType),
                Property("colorName", StringType),
                Property("name", StringType),
            ),
        ),
        Property(
            "scope",
            ObjectType(
                Property("type", StringType),
                Property(
                    "project",
                    ObjectType(
                        Property("id", StringType),
                    ),
                ),
            ),
        ),
    ).to_dict()


class ProjectStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-projects/#api-rest-api-3-project-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "projects"
    path = "/project/search"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[values][*]"  # Or override `parse_response`.
    instance_name = "values"

    schema = PropertiesList(
        Property("expand", StringType),
        Property("self", StringType),
        Property("id", StringType),
        Property("key", StringType),
        Property("name", StringType),
        Property(
            "avatarUrls",
            ObjectType(
                Property("48x48", StringType),
                Property("24x24", StringType),
                Property("16x16", StringType),
                Property("32x32", StringType),
            ),
        ),
        Property("projectTypeKey", StringType),
        Property("simplified", BooleanType),
        Property("style", StringType),
        Property("isPrivate", BooleanType),
        Property(
            "properties",
            ObjectType(
                Property("propertyKey", StringType),
            ),
        ),
        Property("entityId", StringType),
        Property("uuid", StringType),
        Property(
            "projectCategory",
            ObjectType(
                Property("self", StringType),
                Property("id", StringType),
                Property("name", StringType),
                Property("description", StringType),
            ),
        ),
        Property(
            "insight",
            ObjectType(
                Property("totalIssueCount", IntegerType),
                Property("lastIssueUpdateTime", StringType),
            ),
        ),
    ).to_dict()


class IssueStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "issues"
    path = "/search?maxResults=1"
    primary_keys = ["id"]
    replication_key = "updated"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[issues][*]"  # Or override `parse_response`.
    instance_name = "issues"

    schema = PropertiesList(
        Property("expand", StringType),
        Property("id", StringType),
        Property("self", StringType),
        Property("key", StringType),
        Property(
            "fields",
            ObjectType(
                Property("statuscategorychangedate", StringType),
                Property(
                    "issuetype",
                    ObjectType(
                        Property("self", StringType),
                        Property("id", StringType),
                        Property("description", StringType),
                        Property("iconUrl", StringType),
                        Property("name", StringType),
                        Property("subtask", BooleanType),
                        Property("avatarId", IntegerType),
                        Property("entityId", StringType),
                        Property("hierarchyLevel", IntegerType),
                    ),
                ),
                Property(
                    "parent",
                    ObjectType(
                        Property("id", StringType),
                        Property("key", StringType),
                        Property("self", StringType),
                        Property(
                            "fields",
                            ObjectType(
                                Property("summary", StringType),
                                Property(
                                    "status",
                                    ObjectType(
                                        Property("description", StringType),
                                        Property("iconUrl", StringType),
                                        Property("id", StringType),
                                        Property("name", StringType),
                                        Property("self", StringType),
                                        Property(
                                            "statusCategory",
                                            ObjectType(
                                                Property("colorName", StringType),
                                                Property("id", IntegerType),
                                                Property("key", StringType),
                                                Property("name", StringType),
                                                Property("self", StringType),
                                            ),
                                        ),
                                    ),
                                ),
                                Property(
                                    "priority",
                                    ObjectType(
                                        Property("self", StringType),
                                        Property("iconUrl", StringType),
                                        Property("name", StringType),
                                        Property("id", StringType),
                                    ),
                                ),
                                Property(
                                    "issuetype",
                                    ObjectType(
                                        Property("self", StringType),
                                        Property("id", StringType),
                                        Property("description", StringType),
                                        Property("iconUrl", StringType),
                                        Property("name", StringType),
                                        Property("subtask", BooleanType),
                                        Property("avatarId", IntegerType),
                                        Property("entityId", StringType),
                                        Property("hierarchyLevel", IntegerType),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
                Property("timespent", IntegerType),
                Property("customfield_10030", ArrayType(StringType)),
                Property("customfield_10031", ArrayType(StringType)),
                Property(
                    "project",
                    ObjectType(
                        Property("self", StringType),
                        Property("id", StringType),
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("projectTypeKey", StringType),
                        Property("simplified", BooleanType),
                        Property(
                            "avatarUrls",
                            ObjectType(
                                Property("48x48", StringType),
                                Property("24x24", StringType),
                                Property("16x16", StringType),
                                Property("32x32", StringType),
                            ),
                        ),
                    ),
                ),
                Property("customfield_10032", StringType),
                Property("fixVersions", ArrayType(StringType)),
                Property("customfield_10033", StringType),
                Property("customfield_10034", StringType),
                Property("aggregatetimespent", IntegerType),
                Property("customfield_10035", StringType),
                Property(
                    "resolution",
                    ObjectType(
                        Property("description", StringType),
                        Property("id", StringType),
                        Property("name", StringType),
                        Property("self", StringType),
                    ),
                ),
                Property("customfield_10036", StringType),
                Property("customfield_10037", StringType),
                Property("resolutiondate", StringType),
                Property("workratio", IntegerType),
                Property(
                    "watches",
                    ObjectType(
                        Property("self", StringType),
                        Property("watchCount", IntegerType),
                        Property("isWatching", BooleanType),
                    ),
                ),
                Property("issuerestriction", StringType),
                Property("lastViewed", StringType),
                Property("created", StringType),
                Property(
                    "customfield_10020",
                    ArrayType(
                        ObjectType(
                            Property("boardId", IntegerType),
                            Property("completeDate", StringType),
                            Property("endDate", StringType),
                            Property("goal", StringType),
                            Property("id", IntegerType),
                            Property("name", StringType),
                            Property("startDate", StringType),
                            Property("state", StringType),
                        ),
                    ),
                ),
                Property(
                    "customfield_10021",
                    ArrayType(
                        ObjectType(
                            Property("id", StringType),
                            Property("self", StringType),
                            Property("value", StringType),
                        ),
                    ),
                ),
                Property("customfield_10022", StringType),
                Property("customfield_10023", StringType),
                Property(
                    "priority",
                    ObjectType(
                        Property("self", StringType),
                        Property("iconUrl", StringType),
                        Property("name", StringType),
                        Property("id", StringType),
                    ),
                ),
                Property("customfield_10024", StringType),
                Property("customfield_10025", StringType),
                Property("labels", ArrayType(StringType)),
                Property("customfield_10016", NumberType),
                Property("customfield_10017", StringType),
                Property(
                    "customfield_10018",
                    ObjectType(
                        Property("hasEpicLinkFieldDependency", BooleanType),
                        Property("showField", BooleanType),
                        Property(
                            "nonEditableReason",
                            ObjectType(
                                Property("reason", StringType),
                                Property("message", StringType),
                            ),
                        ),
                    ),
                ),
                Property("customfield_10019", StringType),
                Property("timeestimate", IntegerType),
                Property("aggregatetimeoriginalestimate", IntegerType),
                Property("versions", ArrayType(StringType)),
                Property(
                    "issuelinks",
                    ArrayType(
                        ObjectType(
                            Property("id", StringType),
                            Property(
                                "outwardIssue",
                                ObjectType(
                                    Property(
                                        "fields",
                                        ObjectType(
                                            Property(
                                                "issuetype",
                                                ObjectType(
                                                    Property("avatarId", IntegerType),
                                                    Property("description", StringType),
                                                    Property("entityId", StringType),
                                                    Property(
                                                        "hierarchyLevel", IntegerType
                                                    ),
                                                    Property("iconUrl", StringType),
                                                    Property("id", StringType),
                                                    Property("name", StringType),
                                                    Property("self", StringType),
                                                    Property("subtask", BooleanType),
                                                ),
                                            ),
                                            Property(
                                                "priority",
                                                ObjectType(
                                                    Property("iconUrl", StringType),
                                                    Property("id", StringType),
                                                    Property("name", StringType),
                                                    Property("self", StringType),
                                                ),
                                            ),
                                            Property(
                                                "status",
                                                ObjectType(
                                                    Property("description", StringType),
                                                    Property("iconUrl", StringType),
                                                    Property("id", StringType),
                                                    Property("name", StringType),
                                                    Property("self", StringType),
                                                    Property(
                                                        "statusCategory",
                                                        ObjectType(
                                                            Property(
                                                                "colorName", StringType
                                                            ),
                                                            Property("id", IntegerType),
                                                            Property("key", StringType),
                                                            Property(
                                                                "name", StringType
                                                            ),
                                                            Property(
                                                                "self", StringType
                                                            ),
                                                        ),
                                                    ),
                                                ),
                                            ),
                                            Property("summary", StringType),
                                        ),
                                    ),
                                    Property("id", StringType),
                                    Property("key", StringType),
                                    Property("self", StringType),
                                ),
                            ),
                            Property(
                                "inwardIssue",
                                ObjectType(
                                    Property(
                                        "fields",
                                        ObjectType(
                                            Property(
                                                "issuetype",
                                                ObjectType(
                                                    Property("avatarId", IntegerType),
                                                    Property("description", StringType),
                                                    Property("entityId", StringType),
                                                    Property(
                                                        "hierarchyLevel", IntegerType
                                                    ),
                                                    Property("iconUrl", StringType),
                                                    Property("id", StringType),
                                                    Property("name", StringType),
                                                    Property("self", StringType),
                                                    Property("subtask", BooleanType),
                                                ),
                                            ),
                                            Property(
                                                "priority",
                                                ObjectType(
                                                    Property("iconUrl", StringType),
                                                    Property("id", StringType),
                                                    Property("name", StringType),
                                                    Property("self", StringType),
                                                ),
                                            ),
                                            Property(
                                                "status",
                                                ObjectType(
                                                    Property("description", StringType),
                                                    Property("iconUrl", StringType),
                                                    Property("id", StringType),
                                                    Property("name", StringType),
                                                    Property("self", StringType),
                                                    Property(
                                                        "statusCategory",
                                                        ObjectType(
                                                            Property(
                                                                "colorName", StringType
                                                            ),
                                                            Property("id", IntegerType),
                                                            Property("key", StringType),
                                                            Property(
                                                                "name", StringType
                                                            ),
                                                            Property(
                                                                "self", StringType
                                                            ),
                                                        ),
                                                    ),
                                                ),
                                            ),
                                            Property("summary", StringType),
                                        ),
                                    ),
                                    Property("id", StringType),
                                    Property("key", StringType),
                                    Property("self", StringType),
                                ),
                            ),
                            Property("self", StringType),
                            Property(
                                "type",
                                ObjectType(
                                    Property("id", StringType),
                                    Property("inward", StringType),
                                    Property("name", StringType),
                                    Property("outward", StringType),
                                    Property("self", StringType),
                                ),
                            ),
                        ),
                    ),
                ),
                Property(
                    "assignee",
                    ObjectType(
                        Property("self", StringType),
                        Property("accountId", StringType),
                        Property(
                            "avatarUrls",
                            ObjectType(
                                Property("48x48", StringType),
                                Property("24x24", StringType),
                                Property("16x16", StringType),
                                Property("32x32", StringType),
                            ),
                        ),
                        Property("displayName", StringType),
                        Property("active", BooleanType),
                        Property("timeZone", StringType),
                        Property("accountType", StringType),
                        Property("emailAddress", StringType),
                    ),
                ),
                Property("updated", StringType),
                Property(
                    "status",
                    ObjectType(
                        Property("self", StringType),
                        Property("description", StringType),
                        Property("iconUrl", StringType),
                        Property("name", StringType),
                        Property("id", StringType),
                        Property(
                            "statusCategory",
                            ObjectType(
                                Property("self", StringType),
                                Property("id", IntegerType),
                                Property("key", StringType),
                                Property("colorName", StringType),
                                Property("name", StringType),
                            ),
                        ),
                    ),
                ),
                Property("components", ArrayType(StringType)),
                Property("timeoriginalestimate", IntegerType),
                Property(
                    "description",
                    ObjectType(
                        Property("version", IntegerType),
                        Property("text", StringType),
                        Property("type", StringType),
                        Property(
                            "content",
                            ArrayType(
                                ObjectType(
                                    Property("version", IntegerType),
                                    Property("text", StringType),
                                    Property("type", StringType),
                                    Property(
                                        "attrs",
                                        ObjectType(
                                            Property("href", StringType),
                                            Property("language", StringType),
                                            Property("timestamp", StringType),
                                            Property("colspan", IntegerType),
                                            Property("alt", StringType),
                                            Property(
                                                "colwidth", ArrayType(IntegerType)
                                            ),
                                            Property("background", StringType),
                                            Property("color", StringType),
                                            Property(
                                                "isNumberColumnEnabled", BooleanType
                                            ),
                                            Property("localId", StringType),
                                            Property("panelType", StringType),
                                            Property("level", IntegerType),
                                            Property("accessLevel", StringType),
                                            Property("style", StringType),
                                            Property("text", StringType),
                                            Property("order", IntegerType),
                                            Property("shortName", StringType),
                                            Property("url", StringType),
                                            Property("layout", StringType),
                                            Property("id", StringType),
                                            Property("type", StringType),
                                            Property("collection", StringType),
                                            Property("width", NumberType),
                                            Property("height", NumberType),
                                            Property("occurrenceKey", StringType),
                                        ),
                                    ),
                                    Property(
                                        "marks",
                                        ArrayType(
                                            ObjectType(
                                                Property("type", StringType),
                                                Property(
                                                    "attrs",
                                                    ObjectType(
                                                        Property("href", StringType),
                                                        Property(
                                                            "colspan", IntegerType
                                                        ),
                                                        Property("alt", StringType),
                                                        Property(
                                                            "timestamp", StringType
                                                        ),
                                                        Property(
                                                            "language", StringType
                                                        ),
                                                        Property(
                                                            "colwidth",
                                                            ArrayType(IntegerType),
                                                        ),
                                                        Property(
                                                            "background", StringType
                                                        ),
                                                        Property(
                                                            "isNumberColumnEnabled",
                                                            BooleanType,
                                                        ),
                                                        Property("localId", StringType),
                                                        Property("color", StringType),
                                                        Property(
                                                            "panelType", StringType
                                                        ),
                                                        Property("level", IntegerType),
                                                        Property(
                                                            "accessLevel", StringType
                                                        ),
                                                        Property("style", StringType),
                                                        Property("order", IntegerType),
                                                        Property("text", StringType),
                                                        Property(
                                                            "shortName", StringType
                                                        ),
                                                        Property("url", StringType),
                                                        Property("layout", StringType),
                                                        Property("id", StringType),
                                                        Property("type", StringType),
                                                        Property(
                                                            "collection", StringType
                                                        ),
                                                        Property("width", NumberType),
                                                        Property("height", NumberType),
                                                        Property(
                                                            "occurrenceKey", StringType
                                                        ),
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                    Property(
                                        "content",
                                        ArrayType(
                                            ObjectType(
                                                Property("version", IntegerType),
                                                Property("text", StringType),
                                                Property("type", StringType),
                                                Property(
                                                    "attrs",
                                                    ObjectType(
                                                        Property("href", StringType),
                                                        Property(
                                                            "colspan", IntegerType
                                                        ),
                                                        Property("alt", StringType),
                                                        Property(
                                                            "timestamp", StringType
                                                        ),
                                                        Property(
                                                            "colwidth",
                                                            ArrayType(IntegerType),
                                                        ),
                                                        Property(
                                                            "language", StringType
                                                        ),
                                                        Property(
                                                            "background", StringType
                                                        ),
                                                        Property(
                                                            "isNumberColumnEnabled",
                                                            BooleanType,
                                                        ),
                                                        Property("localId", StringType),
                                                        Property("color", StringType),
                                                        Property(
                                                            "panelType", StringType
                                                        ),
                                                        Property("level", IntegerType),
                                                        Property(
                                                            "accessLevel", StringType
                                                        ),
                                                        Property("style", StringType),
                                                        Property("order", IntegerType),
                                                        Property("text", StringType),
                                                        Property(
                                                            "shortName", StringType
                                                        ),
                                                        Property("url", StringType),
                                                        Property("layout", StringType),
                                                        Property("id", StringType),
                                                        Property("type", StringType),
                                                        Property(
                                                            "collection", StringType
                                                        ),
                                                        Property("width", NumberType),
                                                        Property("height", NumberType),
                                                        Property(
                                                            "occurrenceKey", StringType
                                                        ),
                                                    ),
                                                ),
                                                Property(
                                                    "marks",
                                                    ArrayType(
                                                        ObjectType(
                                                            Property(
                                                                "type", StringType
                                                            ),
                                                            Property(
                                                                "attrs",
                                                                ObjectType(
                                                                    Property(
                                                                        "href",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "colspan",
                                                                        IntegerType,
                                                                    ),
                                                                    Property(
                                                                        "alt",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "timestamp",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "colwidth",
                                                                        ArrayType(
                                                                            IntegerType
                                                                        ),
                                                                    ),
                                                                    Property(
                                                                        "language",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "background",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "isNumberColumnEnabled",
                                                                        BooleanType,
                                                                    ),
                                                                    Property(
                                                                        "localId",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "color",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "panelType",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "level",
                                                                        IntegerType,
                                                                    ),
                                                                    Property(
                                                                        "accessLevel",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "style",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "order",
                                                                        IntegerType,
                                                                    ),
                                                                    Property(
                                                                        "text",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "shortName",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "url",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "layout",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "id", StringType
                                                                    ),
                                                                    Property(
                                                                        "type",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "collection",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "width",
                                                                        NumberType,
                                                                    ),
                                                                    Property(
                                                                        "height",
                                                                        NumberType,
                                                                    ),
                                                                    Property(
                                                                        "occurrenceKey",
                                                                        StringType,
                                                                    ),
                                                                ),
                                                            ),
                                                        ),
                                                    ),
                                                ),
                                                Property(
                                                    "content",
                                                    ArrayType(
                                                        ObjectType(
                                                            Property(
                                                                "version", IntegerType
                                                            ),
                                                            Property(
                                                                "text", StringType
                                                            ),
                                                            Property(
                                                                "type", StringType
                                                            ),
                                                            Property(
                                                                "attrs",
                                                                ObjectType(
                                                                    Property(
                                                                        "href",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "colspan",
                                                                        IntegerType,
                                                                    ),
                                                                    Property(
                                                                        "alt",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "timestamp",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "colwidth",
                                                                        ArrayType(
                                                                            IntegerType
                                                                        ),
                                                                    ),
                                                                    Property(
                                                                        "language",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "background",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "isNumberColumnEnabled",
                                                                        BooleanType,
                                                                    ),
                                                                    Property(
                                                                        "localId",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "color",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "panelType",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "level",
                                                                        IntegerType,
                                                                    ),
                                                                    Property(
                                                                        "accessLevel",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "style",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "order",
                                                                        IntegerType,
                                                                    ),
                                                                    Property(
                                                                        "text",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "shortName",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "url",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "layout",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "id", StringType
                                                                    ),
                                                                    Property(
                                                                        "type",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "collection",
                                                                        StringType,
                                                                    ),
                                                                    Property(
                                                                        "width",
                                                                        NumberType,
                                                                    ),
                                                                    Property(
                                                                        "height",
                                                                        NumberType,
                                                                    ),
                                                                    Property(
                                                                        "occurrenceKey",
                                                                        StringType,
                                                                    ),
                                                                ),
                                                            ),
                                                            Property(
                                                                "marks",
                                                                ArrayType(
                                                                    ObjectType(
                                                                        Property(
                                                                            "type",
                                                                            StringType,
                                                                        ),
                                                                        Property(
                                                                            "attrs",
                                                                            ObjectType(
                                                                                Property(
                                                                                    "href",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "colspan",
                                                                                    IntegerType,
                                                                                ),
                                                                                Property(
                                                                                    "alt",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "timestamp",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "colwidth",
                                                                                    ArrayType(
                                                                                        IntegerType
                                                                                    ),
                                                                                ),
                                                                                Property(
                                                                                    "language",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "background",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "isNumberColumnEnabled",
                                                                                    BooleanType,
                                                                                ),
                                                                                Property(
                                                                                    "localId",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "color",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "panelType",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "level",
                                                                                    IntegerType,
                                                                                ),
                                                                                Property(
                                                                                    "accessLevel",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "style",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "order",
                                                                                    IntegerType,
                                                                                ),
                                                                                Property(
                                                                                    "text",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "shortName",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "url",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "layout",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "id",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "type",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "collection",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "width",
                                                                                    NumberType,
                                                                                ),
                                                                                Property(
                                                                                    "height",
                                                                                    NumberType,
                                                                                ),
                                                                                Property(
                                                                                    "occurrenceKey",
                                                                                    StringType,
                                                                                ),
                                                                            ),
                                                                        ),
                                                                    ),
                                                                ),
                                                            ),
                                                            Property(
                                                                "content",
                                                                ArrayType(
                                                                    ObjectType(
                                                                        Property(
                                                                            "version",
                                                                            IntegerType,
                                                                        ),
                                                                        Property(
                                                                            "text",
                                                                            StringType,
                                                                        ),
                                                                        Property(
                                                                            "type",
                                                                            StringType,
                                                                        ),
                                                                        Property(
                                                                            "attrs",
                                                                            ObjectType(
                                                                                Property(
                                                                                    "href",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "colspan",
                                                                                    IntegerType,
                                                                                ),
                                                                                Property(
                                                                                    "alt",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "timestamp",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "colwidth",
                                                                                    ArrayType(
                                                                                        IntegerType
                                                                                    ),
                                                                                ),
                                                                                Property(
                                                                                    "language",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "background",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "isNumberColumnEnabled",
                                                                                    BooleanType,
                                                                                ),
                                                                                Property(
                                                                                    "localId",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "color",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "panelType",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "level",
                                                                                    IntegerType,
                                                                                ),
                                                                                Property(
                                                                                    "accessLevel",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "style",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "order",
                                                                                    IntegerType,
                                                                                ),
                                                                                Property(
                                                                                    "text",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "shortName",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "url",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "layout",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "id",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "type",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "collection",
                                                                                    StringType,
                                                                                ),
                                                                                Property(
                                                                                    "width",
                                                                                    NumberType,
                                                                                ),
                                                                                Property(
                                                                                    "height",
                                                                                    NumberType,
                                                                                ),
                                                                                Property(
                                                                                    "occurrenceKey",
                                                                                    StringType,
                                                                                ),
                                                                            ),
                                                                        ),
                                                                        Property(
                                                                            "marks",
                                                                            ArrayType(
                                                                                ObjectType(
                                                                                    Property(
                                                                                        "type",
                                                                                        StringType,
                                                                                    ),
                                                                                    Property(
                                                                                        "attrs",
                                                                                        ObjectType(
                                                                                            Property(
                                                                                                "href",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "colspan",
                                                                                                IntegerType,
                                                                                            ),
                                                                                            Property(
                                                                                                "alt",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "timestamp",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "colwidth",
                                                                                                ArrayType(
                                                                                                    IntegerType
                                                                                                ),
                                                                                            ),
                                                                                            Property(
                                                                                                "language",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "background",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "isNumberColumnEnabled",
                                                                                                BooleanType,
                                                                                            ),
                                                                                            Property(
                                                                                                "localId",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "color",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "panelType",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "level",
                                                                                                IntegerType,
                                                                                            ),
                                                                                            Property(
                                                                                                "accessLevel",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "style",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "order",
                                                                                                IntegerType,
                                                                                            ),
                                                                                            Property(
                                                                                                "text",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "shortName",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "url",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "layout",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "id",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "type",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "collection",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "width",
                                                                                                NumberType,
                                                                                            ),
                                                                                            Property(
                                                                                                "height",
                                                                                                NumberType,
                                                                                            ),
                                                                                            Property(
                                                                                                "occurrenceKey",
                                                                                                StringType,
                                                                                            ),
                                                                                        ),
                                                                                    ),
                                                                                ),
                                                                            ),
                                                                        ),
                                                                        Property(
                                                                            "content",
                                                                            ArrayType(
                                                                                ObjectType(
                                                                                    Property(
                                                                                        "version",
                                                                                        IntegerType,
                                                                                    ),
                                                                                    Property(
                                                                                        "text",
                                                                                        StringType,
                                                                                    ),
                                                                                    Property(
                                                                                        "type",
                                                                                        StringType,
                                                                                    ),
                                                                                    Property(
                                                                                        "attrs",
                                                                                        ObjectType(
                                                                                            Property(
                                                                                                "href",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "colspan",
                                                                                                IntegerType,
                                                                                            ),
                                                                                            Property(
                                                                                                "alt",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "timestamp",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "colwidth",
                                                                                                ArrayType(
                                                                                                    IntegerType
                                                                                                ),
                                                                                            ),
                                                                                            Property(
                                                                                                "language",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "background",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "isNumberColumnEnabled",
                                                                                                BooleanType,
                                                                                            ),
                                                                                            Property(
                                                                                                "localId",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "color",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "panelType",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "level",
                                                                                                IntegerType,
                                                                                            ),
                                                                                            Property(
                                                                                                "accessLevel",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "style",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "order",
                                                                                                IntegerType,
                                                                                            ),
                                                                                            Property(
                                                                                                "text",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "shortName",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "url",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "layout",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "id",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "type",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "collection",
                                                                                                StringType,
                                                                                            ),
                                                                                            Property(
                                                                                                "width",
                                                                                                NumberType,
                                                                                            ),
                                                                                            Property(
                                                                                                "height",
                                                                                                NumberType,
                                                                                            ),
                                                                                            Property(
                                                                                                "occurrenceKey",
                                                                                                StringType,
                                                                                            ),
                                                                                        ),
                                                                                    ),
                                                                                    Property(
                                                                                        "marks",
                                                                                        ArrayType(
                                                                                            ObjectType(
                                                                                                Property(
                                                                                                    "type",
                                                                                                    StringType,
                                                                                                ),
                                                                                                Property(
                                                                                                    "attrs",
                                                                                                    ObjectType(
                                                                                                        Property(
                                                                                                            "href",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "colspan",
                                                                                                            IntegerType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "alt",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "timestamp",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "language",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "colwidth",
                                                                                                            ArrayType(
                                                                                                                IntegerType
                                                                                                            ),
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "background",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "isNumberColumnEnabled",
                                                                                                            BooleanType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "localId",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "color",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "panelType",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "level",
                                                                                                            IntegerType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "accessLevel",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "style",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "order",
                                                                                                            IntegerType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "text",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "shortName",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "url",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "layout",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "id",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "type",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "collection",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "width",
                                                                                                            NumberType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "height",
                                                                                                            NumberType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "occurrenceKey",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                    ),
                                                                                                ),
                                                                                            ),
                                                                                        ),
                                                                                    ),
                                                                                    Property(
                                                                                        "content",
                                                                                        ArrayType(
                                                                                            ObjectType(
                                                                                                Property(
                                                                                                    "version",
                                                                                                    IntegerType,
                                                                                                ),
                                                                                                Property(
                                                                                                    "text",
                                                                                                    StringType,
                                                                                                ),
                                                                                                Property(
                                                                                                    "type",
                                                                                                    StringType,
                                                                                                ),
                                                                                                Property(
                                                                                                    "attrs",
                                                                                                    ObjectType(
                                                                                                        Property(
                                                                                                            "href",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "colspan",
                                                                                                            IntegerType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "alt",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "timestamp",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "language",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "colwidth",
                                                                                                            ArrayType(
                                                                                                                IntegerType
                                                                                                            ),
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "background",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "isNumberColumnEnabled",
                                                                                                            BooleanType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "localId",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "color",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "panelType",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "level",
                                                                                                            IntegerType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "accessLevel",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "style",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "order",
                                                                                                            IntegerType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "text",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "shortName",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "url",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "layout",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "id",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "type",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "collection",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "width",
                                                                                                            NumberType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "height",
                                                                                                            NumberType,
                                                                                                        ),
                                                                                                        Property(
                                                                                                            "occurrenceKey",
                                                                                                            StringType,
                                                                                                        ),
                                                                                                    ),
                                                                                                ),
                                                                                                Property(
                                                                                                    "marks",
                                                                                                    ArrayType(
                                                                                                        ObjectType(
                                                                                                            Property(
                                                                                                                "type",
                                                                                                                StringType,
                                                                                                            ),
                                                                                                            Property(
                                                                                                                "attrs",
                                                                                                                ObjectType(
                                                                                                                    Property(
                                                                                                                        "href",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "colspan",
                                                                                                                        IntegerType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "alt",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "timestamp",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "language",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "colwidth",
                                                                                                                        ArrayType(
                                                                                                                            IntegerType
                                                                                                                        ),
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "background",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "isNumberColumnEnabled",
                                                                                                                        BooleanType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "localId",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "color",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "panelType",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "level",
                                                                                                                        IntegerType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "accessLevel",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "style",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "order",
                                                                                                                        IntegerType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "text",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "shortName",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "url",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "layout",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "id",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "type",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "collection",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "width",
                                                                                                                        NumberType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "height",
                                                                                                                        NumberType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "occurrenceKey",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                ),
                                                                                                            ),
                                                                                                        ),
                                                                                                    ),
                                                                                                ),
                                                                                                Property(
                                                                                                    "content",
                                                                                                    ArrayType(
                                                                                                        ObjectType(
                                                                                                            Property(
                                                                                                                "version",
                                                                                                                IntegerType,
                                                                                                            ),
                                                                                                            Property(
                                                                                                                "text",
                                                                                                                StringType,
                                                                                                            ),
                                                                                                            Property(
                                                                                                                "type",
                                                                                                                StringType,
                                                                                                            ),
                                                                                                            Property(
                                                                                                                "attrs",
                                                                                                                ObjectType(
                                                                                                                    Property(
                                                                                                                        "href",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "colspan",
                                                                                                                        IntegerType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "alt",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "timestamp",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "language",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "colwidth",
                                                                                                                        ArrayType(
                                                                                                                            IntegerType
                                                                                                                        ),
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "background",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "isNumberColumnEnabled",
                                                                                                                        BooleanType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "localId",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "color",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "panelType",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "level",
                                                                                                                        IntegerType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "accessLevel",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "style",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "order",
                                                                                                                        IntegerType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "text",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "shortName",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "url",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "layout",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "id",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "type",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "collection",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "width",
                                                                                                                        NumberType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "height",
                                                                                                                        NumberType,
                                                                                                                    ),
                                                                                                                    Property(
                                                                                                                        "occurrenceKey",
                                                                                                                        StringType,
                                                                                                                    ),
                                                                                                                ),
                                                                                                            ),
                                                                                                            Property(
                                                                                                                "marks",
                                                                                                                ArrayType(
                                                                                                                    ObjectType(
                                                                                                                        Property(
                                                                                                                            "type",
                                                                                                                            StringType,
                                                                                                                        ),
                                                                                                                        Property(
                                                                                                                            "attrs",
                                                                                                                            ObjectType(
                                                                                                                                Property(
                                                                                                                                    "href",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "colspan",
                                                                                                                                    IntegerType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "alt",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "timestamp",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "language",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "colwidth",
                                                                                                                                    ArrayType(
                                                                                                                                        IntegerType
                                                                                                                                    ),
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "background",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "isNumberColumnEnabled",
                                                                                                                                    BooleanType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "localId",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "color",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "panelType",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "level",
                                                                                                                                    IntegerType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "accessLevel",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "style",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "order",
                                                                                                                                    IntegerType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "text",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "shortName",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "url",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "layout",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "id",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "type",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "collection",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "width",
                                                                                                                                    NumberType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "height",
                                                                                                                                    NumberType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "occurrenceKey",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                            ),
                                                                                                                        ),
                                                                                                                    ),
                                                                                                                ),
                                                                                                            ),
                                                                                                            Property(
                                                                                                                "content",
                                                                                                                ArrayType(
                                                                                                                    ObjectType(
                                                                                                                        Property(
                                                                                                                            "version",
                                                                                                                            IntegerType,
                                                                                                                        ),
                                                                                                                        Property(
                                                                                                                            "text",
                                                                                                                            StringType,
                                                                                                                        ),
                                                                                                                        Property(
                                                                                                                            "type",
                                                                                                                            StringType,
                                                                                                                        ),
                                                                                                                        Property(
                                                                                                                            "attrs",
                                                                                                                            ObjectType(
                                                                                                                                Property(
                                                                                                                                    "href",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "colspan",
                                                                                                                                    IntegerType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "alt",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "timestamp",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "language",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "colwidth",
                                                                                                                                    ArrayType(
                                                                                                                                        IntegerType
                                                                                                                                    ),
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "background",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "isNumberColumnEnabled",
                                                                                                                                    BooleanType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "localId",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "color",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "panelType",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "level",
                                                                                                                                    IntegerType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "accessLevel",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "style",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "order",
                                                                                                                                    IntegerType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "text",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "shortName",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "url",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "layout",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "id",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "type",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "collection",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "width",
                                                                                                                                    NumberType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "height",
                                                                                                                                    NumberType,
                                                                                                                                ),
                                                                                                                                Property(
                                                                                                                                    "occurrenceKey",
                                                                                                                                    StringType,
                                                                                                                                ),
                                                                                                                            ),
                                                                                                                        ),
                                                                                                                        Property(
                                                                                                                            "marks",
                                                                                                                            ArrayType(
                                                                                                                                ObjectType(
                                                                                                                                    Property(
                                                                                                                                        "type",
                                                                                                                                        StringType,
                                                                                                                                    ),
                                                                                                                                    Property(
                                                                                                                                        "attrs",
                                                                                                                                        ObjectType(
                                                                                                                                            Property(
                                                                                                                                                "href",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "colspan",
                                                                                                                                                IntegerType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "alt",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "timestamp",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "language",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "colwidth",
                                                                                                                                                ArrayType(
                                                                                                                                                    IntegerType
                                                                                                                                                ),
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "background",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "isNumberColumnEnabled",
                                                                                                                                                BooleanType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "localId",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "color",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "panelType",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "level",
                                                                                                                                                IntegerType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "accessLevel",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "style",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "order",
                                                                                                                                                IntegerType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "text",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "shortName",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "url",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "layout",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "id",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "type",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "collection",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "width",
                                                                                                                                                NumberType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "height",
                                                                                                                                                NumberType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "occurrenceKey",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                        ),
                                                                                                                                    ),
                                                                                                                                ),
                                                                                                                            ),
                                                                                                                        ),
                                                                                                                        Property(
                                                                                                                            "content",
                                                                                                                            ArrayType(
                                                                                                                                ObjectType(
                                                                                                                                    Property(
                                                                                                                                        "version",
                                                                                                                                        IntegerType,
                                                                                                                                    ),
                                                                                                                                    Property(
                                                                                                                                        "text",
                                                                                                                                        StringType,
                                                                                                                                    ),
                                                                                                                                    Property(
                                                                                                                                        "type",
                                                                                                                                        StringType,
                                                                                                                                    ),
                                                                                                                                    Property(
                                                                                                                                        "attrs",
                                                                                                                                        ObjectType(
                                                                                                                                            Property(
                                                                                                                                                "href",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "colspan",
                                                                                                                                                IntegerType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "alt",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "timestamp",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "language",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "colwidth",
                                                                                                                                                ArrayType(
                                                                                                                                                    IntegerType
                                                                                                                                                ),
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "background",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "isNumberColumnEnabled",
                                                                                                                                                BooleanType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "localId",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "color",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "panelType",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "level",
                                                                                                                                                IntegerType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "accessLevel",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "style",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "order",
                                                                                                                                                IntegerType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "text",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "shortName",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "url",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "layout",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "id",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "type",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "collection",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "width",
                                                                                                                                                NumberType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "height",
                                                                                                                                                NumberType,
                                                                                                                                            ),
                                                                                                                                            Property(
                                                                                                                                                "occurrenceKey",
                                                                                                                                                StringType,
                                                                                                                                            ),
                                                                                                                                        ),
                                                                                                                                    ),
                                                                                                                                    Property(
                                                                                                                                        "marks",
                                                                                                                                        ArrayType(
                                                                                                                                            ObjectType(
                                                                                                                                                Property(
                                                                                                                                                    "type",
                                                                                                                                                    StringType,
                                                                                                                                                ),
                                                                                                                                                Property(
                                                                                                                                                    "attrs",
                                                                                                                                                    ObjectType(
                                                                                                                                                        Property(
                                                                                                                                                            "href",
                                                                                                                                                            StringType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "colspan",
                                                                                                                                                            IntegerType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "alt",
                                                                                                                                                            StringType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "timestamp",
                                                                                                                                                            StringType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "language",
                                                                                                                                                            StringType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "colwidth",
                                                                                                                                                            ArrayType(
                                                                                                                                                                IntegerType
                                                                                                                                                            ),
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "background",
                                                                                                                                                            StringType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "isNumberColumnEnabled",
                                                                                                                                                            BooleanType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "localId",
                                                                                                                                                            StringType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "color",
                                                                                                                                                            StringType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "panelType",
                                                                                                                                                            StringType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "level",
                                                                                                                                                            IntegerType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "accessLevel",
                                                                                                                                                            StringType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "style",
                                                                                                                                                            StringType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "order",
                                                                                                                                                            IntegerType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "text",
                                                                                                                                                            StringType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "shortName",
                                                                                                                                                            StringType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "url",
                                                                                                                                                            StringType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "layout",
                                                                                                                                                            StringType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "id",
                                                                                                                                                            StringType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "type",
                                                                                                                                                            StringType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "collection",
                                                                                                                                                            StringType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "width",
                                                                                                                                                            NumberType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "height",
                                                                                                                                                            NumberType,
                                                                                                                                                        ),
                                                                                                                                                        Property(
                                                                                                                                                            "occurrenceKey",
                                                                                                                                                            StringType,
                                                                                                                                                        ),
                                                                                                                                                    ),
                                                                                                                                                ),
                                                                                                                                            ),
                                                                                                                                        ),
                                                                                                                                    ),
                                                                                                                                ),
                                                                                                                            ),
                                                                                                                        ),
                                                                                                                    ),
                                                                                                                ),
                                                                                                            ),
                                                                                                        ),
                                                                                                    ),
                                                                                                ),
                                                                                            ),
                                                                                        ),
                                                                                    ),
                                                                                ),
                                                                            ),
                                                                        ),
                                                                    ),
                                                                ),
                                                            ),
                                                        ),
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
                Property("customfield_10010", StringType),
                Property("customfield_10014", StringType),
                Property("timetracking", StringType),
                Property("customfield_10015", StringType),
                Property("customfield_10005", StringType),
                Property("customfield_10006", StringType),
                Property("customfield_10007", StringType),
                Property("security", StringType),
                Property("customfield_10008", StringType),
                Property("aggregatetimeestimate", IntegerType),
                Property("customfield_10009", StringType),
                Property("attachment", ArrayType(StringType)),
                Property("summary", StringType),
                Property(
                    "creator",
                    ObjectType(
                        Property("self", StringType),
                        Property("accountId", StringType),
                        Property("emailAddress", StringType),
                        Property(
                            "avatarUrls",
                            ObjectType(
                                Property("48x48", StringType),
                                Property("24x24", StringType),
                                Property("16x16", StringType),
                                Property("32x32", StringType),
                            ),
                        ),
                        Property("displayName", StringType),
                        Property("active", BooleanType),
                        Property("timeZone", StringType),
                        Property("accountType", StringType),
                    ),
                ),
                Property(
                    "subtasks",
                    ArrayType(
                        ObjectType(
                            Property("id", StringType),
                            Property("key", StringType),
                            Property("self", StringType),
                            Property(
                                "fields",
                                ObjectType(
                                    Property("summary", StringType),
                                    Property(
                                        "status",
                                        ObjectType(
                                            Property("self", StringType),
                                            Property("description", StringType),
                                            Property("iconUrl", StringType),
                                            Property("name", StringType),
                                            Property("id", StringType),
                                            Property(
                                                "statusCategory",
                                                ObjectType(
                                                    Property("self", StringType),
                                                    Property("id", IntegerType),
                                                    Property("key", StringType),
                                                    Property("colorName", StringType),
                                                    Property("name", StringType),
                                                ),
                                            ),
                                        ),
                                    ),
                                    Property(
                                        "priority",
                                        ObjectType(
                                            Property("self", StringType),
                                            Property("iconUrl", StringType),
                                            Property("name", StringType),
                                            Property("id", StringType),
                                        ),
                                    ),
                                    Property(
                                        "issuetype",
                                        ObjectType(
                                            Property("self", StringType),
                                            Property("id", StringType),
                                            Property("description", StringType),
                                            Property("iconUrl", StringType),
                                            Property("name", StringType),
                                            Property("subtask", BooleanType),
                                            Property("avatarId", IntegerType),
                                            Property("entityId", StringType),
                                            Property("hierarchyLevel", IntegerType),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
                Property("customfield_10041", StringType),
                Property(
                    "reporter",
                    ObjectType(
                        Property("self", StringType),
                        Property("accountId", StringType),
                        Property("emailAddress", StringType),
                        Property(
                            "avatarUrls",
                            ObjectType(
                                Property("48x48", StringType),
                                Property("24x24", StringType),
                                Property("16x16", StringType),
                                Property("32x32", StringType),
                            ),
                        ),
                        Property("displayName", StringType),
                        Property("active", BooleanType),
                        Property("timeZone", StringType),
                        Property("accountType", StringType),
                    ),
                ),
                Property("customfield_10043", StringType),
                Property("customfield_10044", StringType),
                Property(
                    "aggregateprogress",
                    ObjectType(
                        Property("progress", IntegerType),
                        Property("total", IntegerType),
                        Property("percent", IntegerType),
                    ),
                ),
                Property("customfield_10045", StringType),
                Property("customfield_10001", StringType),
                Property("customfield_10002", StringType),
                Property("customfield_10003", StringType),
                Property("customfield_10004", StringType),
                Property("customfield_10038", StringType),
                Property("customfield_10039", StringType),
                Property("customfield_10000", StringType),
                Property("customfield_10042", StringType),
                Property("customfield_10046", StringType),
                Property("customfield_10047", StringType),
                Property(
                    "environment",
                    ObjectType(
                        Property("type", StringType),
                        Property(
                            "content",
                            ArrayType(
                                ObjectType(
                                    Property(
                                        "content",
                                        ArrayType(
                                            ObjectType(
                                                Property("text", StringType),
                                                Property("type", StringType),
                                            ),
                                        ),
                                    ),
                                    Property("type", StringType),
                                ),
                            ),
                        ),
                        Property("text", StringType),
                        Property("version", IntegerType),
                    ),
                ),
                Property("duedate", StringType),
                Property(
                    "progress",
                    ObjectType(
                        Property("progress", IntegerType),
                        Property("total", IntegerType),
                    ),
                ),
                Property("comment", StringType),
                Property(
                    "votes",
                    ObjectType(
                        Property("self", StringType),
                        Property("votes", IntegerType),
                        Property("hasVoted", BooleanType),
                    ),
                ),
                Property("worklog", StringType),
                Property("key", StringType),
                Property("id", IntegerType),
                Property("editmeta", StringType),
                Property("histories", StringType),
            ),
        ),
        Property("created", StringType),
        Property("updated", StringType),
    ).to_dict()

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        params: dict = {}
        
        params["jql"] = []  # init a query param

        if next_page_token:
            params["startAt"] = next_page_token

        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        if "start_date" in self.config:
            start_date = self.config["start_date"]
            params["jql"].append(f"(created>={start_date} or updated>={start_date})")

        if "end_date" in self.config:
            end_date = self.config["end_date"]
            params["jql"].append(f"(created<{end_date} or updated<{start_date})")

        if params["jql"]:
            jql = " and ".join(params["jql"])
            params["jql"] = jql

        else:
            params.pop("jql") # drop if there's no query

        return params

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        """
        We can add created and updated time columns from field column
        """

        try:
            row["created"] = row.get("fields").get("created")
            row["updated"] = row.get("fields").get("updated")
        except:
            pass

        return super().post_process(row, context)


class PermissionStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-permissions/#api-rest-api-3-permissions-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    name = "permissions"
    path = "/permissions"
    primary_keys = ["permissions"]
    replication_key = "permissions"
    replication_method = "INCREMENTAL"
    instance_name = ""

    schema = PropertiesList(
        Property(
            "permissions",
            ObjectType(
                Property(
                    "ADD_COMMENTS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "ADMINISTER_PROJECTS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "DELETE_ALL_WORKLOGS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "ADMINISTER",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "ADMINISTER_PROJECT",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "ASSIGNABLE_USER",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "ASSIGN_ISSUES",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "BROWSE_PROJECTS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "BULK_CHANGE",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "CLOSE_ISSUES",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "CREATE_ATTACHMENTS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "CREATE_ISSUES",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "CREATE_PROJECT",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "CREATE_SHARED_OBJECTS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "DELETE_ALL_ATTACHMENTS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "DELETE_ALL_COMMENTS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "DELETE_ALL_WORKLOG",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "DELETE_ISSUES",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "DELETE_OWN_ATTACHMENTS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "DELETE_OWN_COMMENTS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "DELETE_OWN_WORKLOGS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "EDIT_ALL_COMMENTS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "EDIT_ALL_WORKLOGS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "EDIT_ISSUES",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "EDIT_OWN_COMMENTS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "EDIT_OWN_WORKLOGS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "LINK_ISSUES",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "MANAGE_GROUP_FILTER_SUBSCRIPTIONS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "MANAGE_SPRINTS_PERMISSION",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "MANAGE_WATCHERS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "MODIFY_REPORTER",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "MOVE_ISSUES",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "RESOLVE_ISSUES",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "SCHEDULE_ISSUES",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "SET_ISSUE_SECURITY",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "SYSTEM_ADMIN",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "TRANSITION_ISSUES",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "USER_PICKER",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "VIEW_AGGREGATED_DATA",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "VIEW_DEV_TOOLS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "VIEW_READONLY_WORKFLOW",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "VIEW_VOTERS_AND_WATCHERS",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "WORK_ON_ISSUES",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
                Property(
                    "com.atlassian.atlas.jira__jira-townsquare-link-unconnected-issue-glance-view-permission",
                    ObjectType(
                        Property("key", StringType),
                        Property("name", StringType),
                        Property("type", StringType),
                        Property("description", StringType),
                    ),
                ),
            ),
        ),
    ).to_dict()


class ProjectRoleStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-roles/#api-rest-api-3-role-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    name = "project_roles"
    path = "/role"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "INCREMENTAL"
    instance_name = ""

    schema = PropertiesList(
        Property("self", StringType),
        Property("name", StringType),
        Property("id", IntegerType),
        Property("description", StringType),
        Property(
            "scope",
            ObjectType(
                Property("type", StringType),
                Property(
                    "project",
                    ObjectType(
                        Property("id", StringType),
                    ),
                ),
            ),
        ),
        Property(
            "actors",
            ArrayType(
                ObjectType(
                    Property("id", IntegerType),
                    Property("displayName", StringType),
                    Property("type", StringType),
                    Property("name", StringType),
                    Property(
                        "actorUser",
                        ObjectType(
                            Property("accountId", StringType),
                        ),
                    ),
                    Property(
                        "actorGroup",
                        ObjectType(
                            Property("name", StringType),
                            Property("displayName", StringType),
                            Property("groupId", StringType),
                        ),
                    ),
                ),
            ),
        ),
    ).to_dict()


class PriorityStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-priorities/#api-rest-api-3-priority-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    name = "priorities"
    path = "/priority"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "INCREMENTAL"
    instance_name = ""

    schema = PropertiesList(
        Property("self", StringType),
        Property("statusColor", StringType),
        Property("description", StringType),
        Property("iconUrl", StringType),
        Property("name", StringType),
        Property("id", StringType),
    ).to_dict()


class PermissionHolderStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-permission-schemes/#api-rest-api-3-permissionscheme-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "permission_holders"
    path = "/permissionscheme"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[permissionSchemes][*]"  # Or override `parse_response`.
    instance_name = "permissionSchemes"

    schema = PropertiesList(
        Property("expand", StringType),
        Property("id", IntegerType),
        Property("self", StringType),
        Property("name", StringType),
        Property(
            "scope",
            ObjectType(
                Property("type", StringType),
                Property(
                    "project",
                    ObjectType(
                        Property("id", StringType),
                    ),
                ),
            ),
        ),
        Property("description", StringType),
        Property(
            "permissions",
            ArrayType(
                ObjectType(
                    Property("id", IntegerType),
                    Property("self", StringType),
                    Property(
                        "holder",
                        ObjectType(
                            Property("type", StringType),
                            Property("parameter", StringType),
                            Property("value", StringType),
                            Property("expand", StringType),
                        ),
                    ),
                    Property("permission", StringType),
                ),
            ),
        ),
    ).to_dict()


class SprintStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference/#sprint
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "sprints"
    path = "/board"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[values][*]"  # Or override `parse_response`.
    instance_name = "values"

    schema = PropertiesList(
        Property("id", IntegerType),
        Property("self", StringType),
        Property("state", StringType),
        Property("name", StringType),
        Property("startDate", StringType),
        Property("endDate", StringType),
        Property("completeDate", StringType),
        Property("originBoardId", IntegerType),
        Property("goal", StringType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        return "https://ryan-miranda.atlassian.net:443/rest/agile/1.0"

    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        """
        Takes each of the board IDs pulled above and makes a request to
        the Sprint endpoint for each board ID
        """

        board_id = []
        sprint_records = []

        for record in list(super().get_records(context)):
            board_id.append(record.get("id"))

        for id in board_id:
            try:

                class Sprint(JiraStream):
                    name = "sprint"
                    path = "/sprint?maxResults=100"
                    instance_name = ""

                    @property
                    def url_base(self) -> str:
                        base_url = "https://ryan-miranda.atlassian.net:443/rest/agile/1.0/board/{}".format(
                            id
                        )
                        return base_url

                    def parse_response(
                        self, response: requests.Response
                    ) -> Iterable[dict]:
                        """Parse the response and return an iterator of result records.

                        Args:
                            response: The HTTP ``requests.Response`` object.

                        Yields:
                            Each record from the source.
                        """

                        resp_json = response.json()

                        if isinstance(resp_json, list):
                            results = resp_json
                        elif resp_json.get("values") is not None:
                            results = resp_json["values"]
                        else:
                            results = resp_json

                        yield from results

                sprint = Sprint(self._tap, schema={"properties": {}})

                sprint_records.append(list(sprint.get_records(context)))

            except:
                pass

        sprint_records = sum(sprint_records, [])

        return sprint_records


class ProjectRoleActorStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-role-actors/#api-rest-api-3-role-id-actors-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    name = "project_role_actors"
    path = "/role"

    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("self", StringType),
        Property("name", StringType),
        Property("id", IntegerType),
        Property("description", StringType),
        Property(
            "actors",
            ArrayType(
                ObjectType(
                    Property("id", IntegerType),
                    Property("displayName", StringType),
                    Property("type", StringType),
                    Property(
                        "actorUser",
                        ObjectType(
                            Property("accountId", StringType),
                        ),
                    ),
                ),
            ),
        ),
        Property(
            "scope",
            ObjectType(
                Property("type", StringType),
                Property(
                    "project",
                    ObjectType(
                        Property("id", StringType),
                    ),
                ),
            ),
        ),
    ).to_dict()

    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        """
        Takes each of the role ID's gathered above and adds to a list, then loops through the
        list and gets data from the project role actor endpoint for each of the role ID's in the list
        """

        role_id = []
        project_id = []
        role_actor_records = []

        project = ProjectStream(self._tap, schema={"properties": {}})

        for record in list(super().get_records(context)):
            role_id.append(record.get("id"))

        for record in list(project.get_records(context)):
            project_id.append(record.get("id"))

        for pid in project_id:
            for role in role_id:
                try:

                    class ProjectRoleActor(JiraStream):
                        role_id = role
                        project_id = pid
                        name = "project_role_actor"
                        path = "/project/{}/role/{}".format(project_id, role_id)
                        instance_name = ""

                    project_role_actor = ProjectRoleActor(
                        self._tap, schema={"properties": {}}
                    )

                    role_actor_records.append(
                        list(project_role_actor.get_records(context))
                    )

                except:
                    pass

        project_role_actor_records = sum(role_actor_records, [])

        return project_role_actor_records


class AuditingStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-audit-records/#api-rest-api-3-auditing-record-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "audit_records"
    path = "/auditing/record"
    primary_keys = ["id"]
    replication_key = "created"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[records][*]"  # Or override `parse_response`.
    instance_name = "records"

    schema = PropertiesList(
        Property("id", IntegerType),
        Property("summary", StringType),
        Property("created", StringType),
        Property("category", StringType),
        Property("eventSource", StringType),
        Property("remoteAddress", StringType),
        Property("authorKey", StringType),
        Property("authorAccountId", StringType),
        Property(
            "objectItem",
            ObjectType(
                Property("id", StringType),
                Property("name", StringType),
                Property("typeName", StringType),
                Property("parentId", StringType),
                Property("parentName", StringType),
            ),
        ),
        Property(
            "changedValues",
            ArrayType(
                ObjectType(
                    Property("fieldName", StringType),
                    Property("changedFrom", StringType),
                    Property("changedTo", StringType),
                ),
            ),
        ),
        Property(
            "associatedItems",
            ArrayType(
                ObjectType(
                    Property("id", StringType),
                    Property("name", StringType),
                    Property("typeName", StringType),
                    Property("parentId", StringType),
                    Property("parentName", StringType),
                ),
            ),
        ),
    ).to_dict()


class DashboardStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-dashboards/#api-rest-api-3-dashboard-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "dashboards"
    path = "/dashboard"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[dashboards][*]"  # Or override `parse_response`.
    instance_name = "dashboards"

    schema = PropertiesList(
        Property("id", StringType),
        Property("isFavourite", BooleanType),
        Property("name", StringType),
        Property("popularity", IntegerType),
        Property("self", StringType),
        Property(
            "sharePermissions",
            ArrayType(
                ObjectType(
                    Property("id", IntegerType),
                    Property("type", StringType),
                ),
            ),
        ),
        Property("editPermissions", ArrayType(StringType)),
        Property("view", StringType),
        Property("isWritable", BooleanType),
        Property("systemDashboard", BooleanType),
    ).to_dict()


class FilterSearchStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-filters/#api-rest-api-3-filter-search-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "filter_searches"
    path = "/filter/search"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[values][*]"  # Or override `parse_response`.
    instance_name = "values"

    schema = PropertiesList(
        Property("expand", StringType),
        Property("self", StringType),
        Property("id", StringType),
        Property("name", StringType),
    ).to_dict()


class FilterDefaultShareScopeStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-filter-sharing/#api-rest-api-3-filter-defaultsharescope-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    name = "filter_default_share_scopes"
    path = "/filter/defaultShareScope"
    primary_keys = ["scope"]
    replication_key = "scope"
    replication_method = "INCREMENTAL"
    instance_name = ""

    schema = PropertiesList(
        Property("scope", StringType),
    ).to_dict()


class GroupsPickerStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-groups/#api-rest-api-3-groups-picker-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath: json response body
    """

    name = "groups_pickers"
    path = "/groups/picker"
    primary_keys = ["groupId"]
    replication_key = "groupId"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[groups][*]"  # Or override `parse_response`.
    instance_name = "groups"

    schema = PropertiesList(
        Property("name", StringType),
        Property("html", StringType),
        Property(
            "labels",
            ArrayType(
                ObjectType(
                    Property("text", StringType),
                    Property("title", StringType),
                    Property("type", StringType),
                ),
            ),
        ),
        Property("groupId", StringType),
    ).to_dict()


class LicenseStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-license-metrics/#api-rest-api-3-instance-license-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "licenses"
    path = "/instance/license"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[applications][*]"  # Or override `parse_response`.
    instance_name = "applications"

    schema = PropertiesList(
        Property("id", StringType),
        Property("plan", StringType),
    ).to_dict()


class ScreensStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-screens/#api-rest-api-3-screens-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "screens"
    path = "/screens"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[values][*]"  # Or override `parse_response`.
    instance_name = "values"

    schema = PropertiesList(
        Property("id", IntegerType),
        Property("name", StringType),
        Property("description", StringType),
        Property(
            "scope",
            ObjectType(
                Property("type", StringType),
                Property(
                    "project",
                    ObjectType(
                        Property("id", StringType),
                    ),
                ),
            ),
        ),
    ).to_dict()


class ScreenSchemesStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-screen-tab-fields/#api-rest-api-3-screens-screenid-tabs-tabid-fields-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "screen_schemes"
    path = "/screenscheme"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[values][*]"  # Or override `parse_response`.
    instance_name = "values"

    schema = PropertiesList(
        Property("id", IntegerType),
        Property("name", StringType),
        Property("description", StringType),
        Property(
            "screens",
            ObjectType(
                Property("default", IntegerType), Property("create", IntegerType)
            ),
        ),
    ).to_dict()


class StatusesSearchStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-screen-tab-fields/#api-rest-api-3-screens-screenid-tabs-tabid-fields-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "statuses_searches"
    path = "/statuses/search"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[values][*]"  # Or override `parse_response`.
    instance_name = "values"

    schema = PropertiesList(
        Property("id", StringType),
        Property("name", StringType),
        Property("statusCategory", StringType),
        Property(
            "scope",
            ObjectType(Property("type", StringType)),
        ),
        Property("description", StringType),
        Property("usages", ArrayType(StringType)),
        Property("workflowUsages", ArrayType(StringType)),
    ).to_dict()


class WorkflowStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-workflows/#api-rest-api-3-workflow-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    name = "workflows"
    path = "/workflow"
    primary_keys = ["name"]
    replication_key = "name"
    replication_method = "INCREMENTAL"
    instance_name = ""

    schema = PropertiesList(
        Property("name", StringType),
        Property("description", StringType),
        Property("steps", IntegerType),
        Property("default", BooleanType),
        Property("lastModifiedDate", StringType),
        Property("lastModifiedUser", StringType),
        Property("lastModifiedUserAccountId", StringType),
        Property(
            "scope",
            ObjectType(
                Property("type", StringType),
                Property(
                    "project",
                    ObjectType(
                        Property("id", StringType),
                    ),
                ),
            ),
        ),
    ).to_dict()


class WorkflowSearchStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-workflows/#api-rest-api-3-workflow-get
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "workflow_searches"
    path = "/workflow/search"
    primary_keys = ["id"]
    replication_key = "updated"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[values][*]"  # Or override `parse_response`.
    instance_name = "values"

    schema = PropertiesList(
        Property(
            "id",
            ObjectType(
                Property("name", StringType),
                Property("entityId", StringType),
            ),
        ),
        Property("description", StringType),
        Property("created", StringType),
        Property("updated", StringType),
    ).to_dict()
