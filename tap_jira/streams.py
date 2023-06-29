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
role = {}

class UsersStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-users/#api-rest-api-3-user-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    columns = """
                 self, accountId, accountType, name, emailAddress, avatarUrls, displayName, active, timeZone, locale, groups, applicationRoles, expand
              """

    name = "user"
    path = "/user"
    primary_keys = ["accountId"]
    replication_key = "accountId"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("self", StringType),
        Property("accountId", StringType),
        Property("accountType", StringType),
        Property("name", StringType),
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
        Property("locale", StringType),
        Property("groups", StringType),
        Property("applicationRoles", StringType),
        Property("expand", StringType),

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

        account_id = self.config.get("account_id", "")

        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        params["accountId"] = account_id

        return params


class FieldStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-fields/#api-rest-api-3-field-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    columns = """
                 id, key, name, untranslatedName, custom, orderable, navigable, searchable, clauseNames, schema, untranslatedName
              """

    name = "field"
    path = "/field"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "incremental"

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
            "schema",
            ObjectType(
                Property("type", StringType),
                Property("system", StringType),
            ),
        ),

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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        resp_json = response.json()

        if isinstance(resp_json, list):
            results = resp_json
        elif resp_json.get("records") is not None:
            results = resp_json["records"]
        else:
            results = resp_json

        yield from results


class ServerInfoStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-server-info/#api-rest-api-3-serverinfo-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    columns = """
                 baseUrl, version, versionNumbers, deploymentType, buildNumber, buildDate, serverTime, scmInfo, serverTitle, defaultLocale
              """

    name = "server_info"
    path = "/serverInfo"
    primary_keys = ["baseUrl"]
    replication_key = "serverTime"
    replication_method = "incremental"

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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params


class IssueTypeStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-types/#api-rest-api-3-issuetype-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    columns = """
                 self, id, description, iconUrl, name, untranslatedName, subtask, avatarId, hierarchyLevel, scope
              """

    name = "issue_type"
    path = "/issuetype"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "incremental"

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
        Property("scope", StringType),

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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        resp_json = response.json()

        if isinstance(resp_json, list):
            results = resp_json
        elif resp_json.get("records") is not None:
            results = resp_json["records"]
        else:
            results = resp_json

        yield from results


class StatusStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-status/#api-rest-api-3-statuses-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    columns = """
                 self, description, iconUrl, name, untranslatedName, id, statusCategory, scope
              """

    name = "status"
    path = "/status"
    primary_keys = ["id"]
    replication_key = "self"
    replication_method = "incremental"

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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params


class ProjectStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-projects/#api-rest-api-3-project-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    columns = """
                 expand, self, id, key, name, avatarUrls, projectTypeKey, simplified, style, isPrivate, properties, entityId, uuid
              """

    name = "project"
    path = "/project"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "incremental"

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
        Property("properties", StringType),
        Property("entityId", StringType),
        Property("uuid", StringType),

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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        resp_json = response.json()

        if isinstance(resp_json, list):
            results = resp_json
        elif resp_json.get("records") is not None:
            results = resp_json["records"]
        else:
            results = resp_json

        yield from results


class IssueStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-issueidorkey-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    issue_out: issue out value
    """

    name = "issue"
    path = "/search"
    primary_keys = ["id"]
    replication_key = "updated"
    replication_method = "incremental"

    schema = PropertiesList(
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
        Property("timespent", StringType),
        Property("customfield_10030", ArrayType(StringType)),
        Property("customfield_10031", ArrayType(StringType)),
        Property(
            "project",
            Property(
                "issuetype",
                ObjectType(
                    Property("self", StringType),
                    Property("id", StringType),
                    Property("key", StringType),
                    Property("name", StringType),
                    Property("ProjectTypeKey", StringType),
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
        ),
        Property("customfield_10032", StringType),
        Property("fixVersions", ArrayType(StringType)),
        Property("customfield_10033", StringType),
        Property("customfield_10034", StringType),
        Property("aggregatetimespent", StringType),
        Property("customfield_10035", StringType),
        Property("resolution", StringType),
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
        Property("customfield_10020", StringType),
        Property("customfield_10021", StringType),
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
        Property("customfield_10016", StringType),
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
        Property("timeestimate", StringType),
        Property("aggregatetimeoriginalestimate", StringType),
        Property("versions", ArrayType(StringType)),
        Property("issuelinks", ArrayType(StringType)),
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
        Property("timeoriginalestimate", StringType),
        Property(
            "description",
            ObjectType(
                Property("version", IntegerType),
                Property("type", StringType),
                Property("content", ArrayType(StringType)),
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
        Property("aggregatetimeestimate", StringType),
        Property("customfield_10009", StringType),
        Property("attachment", ArrayType(StringType)),
        Property("summary", StringType),
        Property(
            "creator",
            ObjectType(
                Property("self", StringType),
                Property("accountId", StringType),
                Property(
                    "avartarUrls",
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
        Property("subtasks", ArrayType(StringType)),
        Property("customfield_10041", StringType),
        Property(
            "reporter",
            ObjectType(
                Property("self", StringType),
                Property("accountId", StringType),
                Property("emailAddress", StringType),
                Property(
                    "avartarUrls",
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
            ),
        ),
        Property("customfield_10045", StringType),
        Property("customfield_10001", StringType),
        Property("customfield_10002", StringType),
        Property("customfield_10003", StringType),
        Property("customfield_10004", StringType),
        Property("customfield_10038", StringType),
        Property("customfield_10039", StringType),
        Property("environment", StringType),
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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        resp_json = response.json()

        if isinstance(resp_json, list):
            results = resp_json
        elif resp_json.get("issues") is not None:
            results = resp_json["issues"]
        else:
            results = resp_json

        yield from results

    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        """
        We have key values for issues (OUT-1 to OUT-26), we have records for each key value
        We can get the records with these key values from the parent IssueSearchWatcherStream and add them to jira_issue_key list
        We can traverse through these key values with a for loop and create a child class for them
        We can get the records for each key value in a child class and then we can join each of them with get records function and add them to jira_issue_records list
        """

        jira_issue_key = []
        jira_issue_records = []

        for record in list(super().get_records(context)):
            jira_issue_key.append(record.get("key"))

        for key in jira_issue_key:

            class IssueKey(JiraStream):
                issues_out = key
                name = "issue"
                path = "/issue/{}/".format(issues_out)

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
                        params["page"] = next_page_token
                    if self.replication_key:
                        params["sort"] = "asc"
                    params["order_by"] = self.replication_key

                    params["expand"] = "editmeta,changelog"

                    return params

                def parse_response(self, response: requests.Response) -> Iterable[dict]:
                    """Parse the response and return an iterator of result records.

                    Args:
                        response: The HTTP ``requests.Response`` object.

                    Yields:
                        Each record from the source.
                    """

                    resp_json = response.json()

                    if isinstance(resp_json, list):
                        results = resp_json
                    elif resp_json.get("fields") is not None:
                        resp_json["fields"]["editmeta"] = resp_json.get("editmeta")
                        resp_json["fields"]["histories"] = resp_json.get("changelog").get("histories")
                        results = [resp_json["fields"]]
                    else:
                        results = resp_json

                    yield from results

                def post_process(self, row: dict, context: dict | None = None) -> dict | None:
                    """
                    We can add a key column which have out value
                    We can get the id from comment column, we have a url in comment column, we can split it by / and get the id from it
                    """

                    try:
                        row["key"] = self.issues_out
                        row["id"] = row.get("comment").get("self").split("/")[7]
                    except:
                        pass

                    return super().post_process(row, context)

            issue_search_key = IssueKey(
                self._tap, schema={"properties": {}}
            )

            jira_issue_records.append(list(issue_search_key.get_records(context)))

        issue_records = sum(jira_issue_records, [])

        return issue_records


class SearchStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    name = "search"
    path = "/search"
    primary_keys = ["id"]
    replication_key = "updated"
    replication_method = "incremental"

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
                Property("timespent", StringType),
                Property("customfield_10030", ArrayType(StringType)),
                Property("customfield_10031", ArrayType(StringType)),
                Property(
                    "project",
                    Property(
                        "issuetype",
                        ObjectType(
                            Property("self", StringType),
                            Property("id", StringType),
                            Property("key", StringType),
                            Property("name", StringType),
                            Property("ProjectTypeKey", StringType),
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
                ),
                Property("customfield_10032", StringType),
                Property("fixVersions", ArrayType(StringType)),
                Property("customfield_10033", StringType),
                Property("customfield_10034", StringType),
                Property("aggregatetimespent", StringType),
                Property("customfield_10035", StringType),
                Property("resolution", StringType),
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
                Property("customfield_10020", StringType),
                Property("customfield_10021", StringType),
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
                Property("customfield_10016", StringType),
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
                Property("timeestimate", StringType),
                Property("aggregatetimeoriginalestimate", StringType),
                Property("versions", ArrayType(StringType)),
                Property("issuelinks", ArrayType(StringType)),
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
                Property("timeoriginalestimate", StringType),
                Property(
                    "description",
                    ObjectType(
                        Property("version", IntegerType),
                        Property("type", StringType),
                        Property("content", ArrayType(StringType)),
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
                Property("aggregatetimeestimate", StringType),
                Property("customfield_10009", StringType),
                Property("attachment", ArrayType(StringType)),
                Property("summary", StringType),
                Property(
                    "creator",
                    ObjectType(
                        Property("self", StringType),
                        Property("accountId", StringType),
                        Property(
                            "avartarUrls",
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
                Property("subtasks", ArrayType(StringType)),
                Property("customfield_10041", StringType),
                Property(
                    "reporter",
                    ObjectType(
                        Property("self", StringType),
                        Property("accountId", StringType),
                        Property("emailAddress", StringType),
                        Property(
                            "avartarUrls",
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
                    ),
                ),
                Property("customfield_10045", StringType),
                Property("customfield_10001", StringType),
                Property("customfield_10002", StringType),
                Property("customfield_10003", StringType),
                Property("customfield_10004", StringType),
                Property("customfield_10038", StringType),
                Property("customfield_10039", StringType),
                Property("environment", StringType),
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
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        resp_json = response.json()

        if isinstance(resp_json, list):
            results = resp_json
        elif resp_json.get("issues") is not None:
            results = resp_json["issues"]
        else:
            results = resp_json

        yield from results

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
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    columns = """
                 permissions
              """

    name = "permission"
    path = "/permissions"
    primary_keys = ["permissions"]
    replication_key = "permissions"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("permissions", StringType),

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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params


class ProjectRoleStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-roles/#api-rest-api-3-role-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    name = "project_role"
    path = "/role"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "incremental"

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
        Property("actors", ArrayType(StringType)),
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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params


class PriorityStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-priorities/#api-rest-api-3-priority-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    name = "priority"
    path = "/priority"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("self", StringType),
        Property("statusColor", StringType),
        Property("description", StringType),
        Property("iconUrl", StringType),
        Property("name", StringType),
        Property("id", StringType),

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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params


class PermissionHolderStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-permission-schemes/#api-rest-api-3-permissionscheme-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    name = "permission_holder"
    path = "/permissionscheme"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "incremental"

    schema = PropertiesList(
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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        resp_json = response.json()

        if isinstance(resp_json, list):
            results = resp_json
        elif resp_json.get("permissionSchemes") is not None:
            results = resp_json["permissionSchemes"][0].get("permissions")
        else:
            results = resp_json

        yield from results


class SprintStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference/#sprint
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    name = "sprint"
    path = "/board"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("id", StringType),
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
        base_url = "https://ryan-miranda.atlassian.net:443/rest/agile/1.0"
        return base_url

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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
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

    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        """
        We have board ids for board, we have records for each board id
        We can get the records with these board ids from the parent SprintStream and add them to board_id list
        We can traverse through these board ids with a for loop and create a child class for them
        We can get the records for each board ids in a child class and then we can join each of them with get records function and add them to sprint_records list
        We have added a try except statment to create child streams for those ids which have data
        """

        board_id = []
        sprint_records = []

        for record in list(super().get_records(context)):
            board_id.append(record.get("id"))

        for id in board_id:

            try:

                class Sprint(JiraStream):
                    name = "sprint"
                    path = "/sprint"

                    @property
                    def url_base(self) -> str:
                        base_url = "https://ryan-miranda.atlassian.net:443/rest/agile/1.0/board/{}".format(id)
                        return base_url

                    def parse_response(self, response: requests.Response) -> Iterable[dict]:
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

                sprint = Sprint(
                    self._tap, schema={"properties": {}}
                )

                sprint_records.append(list(sprint.get_records(context)))

            except:
                pass

        sprint_records = sum(sprint_records, [])

        return sprint_records


class UserGroupStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-users/#api-rest-api-3-user-groups-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    name = "user_group"
    path = "/user/groups"
    primary_keys = ["self"]
    replication_key = "user_id"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("self", StringType),
        Property("accountId", StringType),
        Property("user_id", StringType),
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
        Property("group_name", StringType),
        Property("name", StringType),

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
        account_id = self.config.get("account_id", "")
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        params["accountId"] = account_id

        return params

    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        """
        We have group names for users, we have records for each group name
        We can get the records with these group names from the parent UserGroupStream and add them to user_group_name list
        We can traverse through these group names with a for loop and create a child class for them
        We can get the records for each group names in a child class and then we can join each of them with get records function and add them to group_records list
        We have added a try except statment to create child streams for those ids which have data
        """

        user_group_name = []
        group_records = []

        for record in list(super().get_records(context)):
            user_group_name.append(record.get("name"))

        for name in user_group_name:

            group_name = name

            try:

                class UserGroup(JiraStream):
                    name = "user_group"
                    path = "/group/member?groupname={}".format(group_name)

                    def parse_response(self, response: requests.Response) -> Iterable[dict]:
                        """Parse the response and return an iterator of result records.

                        Args:
                            response: The HTTP ``requests.Response`` object.

                        Yields:
                            Each record from the source.
                        """

                        resp_json = response.json()

                        if isinstance(resp_json, list):
                            results = resp_json
                        elif len(resp_json.get("values")) !=0:
                            results = resp_json["values"]
                        else:
                            results = [resp_json]

                        yield from results

                    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
                        """
                        We can add a group name column with group name variable and a user id column  with account id column
                        """

                        try:
                            row["group_name"] = group_name
                            row["user_id"] = row["accountId"]
                        except:
                            pass

                        return super().post_process(row, context)

                user_group = UserGroup(
                    self._tap, schema={"properties": {}}
                )

                group_records.append(list(user_group.get_records(context)))

            except:
                pass

        usergroup_records = sum(group_records, [])

        return usergroup_records


class ProjectRoleActorStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-role-actors/#api-rest-api-3-role-id-actors-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    """

    name = "project_role_actor"
    path = "/role"

    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("self", StringType),
        Property("name", StringType),
        Property("id", StringType),
        Property("description", StringType),
        Property(
            "actors",
            ObjectType(
                Property("id", IntegerType),
                Property("displayName", StringType),
                Property("type", StringType),
                Property("accountUser", StringType),
                Property(
                    "actorUser",
                    ObjectType(
                        Property("accountId", StringType),
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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        """
        We have role ids for project, we have records for each role id
        We can get the records with these role ids from the parent ProjectRoleActorStream and add them to role_id list
        We can traverse through these role ids with a for loop and create a child class for them
        We can get the records for each role ids in a child class and then we can join each of them with get records function and add them to role_actor_records list
        We have added a try except statment to create child streams for those ids which have data
        """

        role_id = []
        project_id = []
        role_actor_records = []

        project = ProjectStream(
            self._tap, schema={"properties": {}}
        )

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

                    project_role_actor = ProjectRoleActor(
                        self._tap, schema={"properties": {}}
                    )

                    role_actor_records.append(list(project_role_actor.get_records(context)))

                except:
                    pass

        project_role_actor_records = sum(role_actor_records, [])

        return project_role_actor_records


class IssueWatcherStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-watchers/#api-group-issue-watchers
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    issue_out: issue out value
    """

    name = "issue_watcher"
    path = "/search"
    primary_keys = ["key"]
    replication_key = "user_id"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("self", StringType),
        Property("isWatching", BooleanType),
        Property("watchCount", IntegerType),
        Property("watchers", ArrayType(StringType)),
        Property("user_id", StringType),
        Property("key", StringType),


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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        resp_json = response.json()

        if isinstance(resp_json, list):
            results = resp_json
        elif resp_json.get("issues") is not None:
            results = resp_json["issues"]
        else:
            results = resp_json

        yield from results

    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        """
        We have key values for issues (OUT-1 to OUT-26), we have records for each key value
        We can get the records with these key values from the parent IssueSearchWatcherStream and add them to jira_issue_key list
        We can traverse through these key values with a for loop and create a child class for them
        We can get the records for each key value in a child class and then we can join each of them with get records function and add them to jira_issue_records list
        """

        jira_issue_key = []
        jira_issue_records = []

        for record in list(super().get_records(context)):
            jira_issue_key.append(record.get("key"))

        for key in jira_issue_key:

            class IssueKeyWatcher(JiraStream):
                issues_out = key
                name = "issue_watcher"
                path = "/issue/{}/watchers".format(issues_out)

                def post_process(self, row: dict, context: dict | None = None) -> dict | None:
                    """
                    We can add a key column which have out value
                    We can get the user id column from watchers column
                    """

                    try:
                        row["key"] = self.issues_out
                        row["user_id"] = row.get("watchers")[0].get("accountId")
                    except:
                        pass

                    return super().post_process(row, context)

            issue_search_key_watcher = IssueKeyWatcher(
                self._tap, schema={"properties": {}}
            )

            jira_issue_records.append(list(issue_search_key_watcher.get_records(context)))

        issuewatcher_records = sum(jira_issue_records, [])

        return issuewatcher_records


class AuditingStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-audit-records/#api-rest-api-3-auditing-record-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    issue_out: issue out value
    """

    name = "auditing"
    path = "/auditing/record"
    primary_keys = ["id"]
    replication_key = "created"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("id", IntegerType),
        Property("summary", StringType),
        Property("created", StringType),
        Property("category", StringType),
        Property("eventSource", StringType),
        Property(
            "objectItem",
            ObjectType(
                Property("accountId", StringType),
            ),
        ),
        Property("changedValues", ArrayType(StringType)),
        Property("associatedItems", ArrayType(StringType)),

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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        resp_json = response.json()

        if isinstance(resp_json, list):
            results = resp_json
        elif resp_json.get("records") is not None:
            results = resp_json["records"]
        else:
            results = resp_json

        yield from results


class DashboardStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-dashboards/#api-rest-api-3-dashboard-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    issue_out: issue out value
    """

    name = "dashboard"
    path = "/dashboard"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("id", StringType),
        Property("isFavourite", BooleanType),
        Property("name", StringType),
        Property("popularity", IntegerType),
        Property("self", StringType),
        Property("sharePermissions", ArrayType(StringType)),
        Property("editPermissions", ArrayType(StringType)),
        Property("view", StringType),
        Property("isWritable", BooleanType),
        Property("systemDashboard", BooleanType),


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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        resp_json = response.json()

        if isinstance(resp_json, list):
            results = resp_json
        elif resp_json.get("dashboards") is not None:
            results = resp_json["dashboards"]
        else:
            results = resp_json

        yield from results


class FilterSearchStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-filters/#api-rest-api-3-filter-search-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    issue_out: issue out value
    """

    name = "filter_search"
    path = "/filter/search"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("expand", StringType),
        Property("self", StringType),
        Property("id", StringType),
        Property("name", StringType),


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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
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


class FilterDefaultShareScopeStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-filter-sharing/#api-rest-api-3-filter-defaultsharescope-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    issue_out: issue out value
    """

    name = "filter_default_share_scope"
    path = "/filter/defaultShareScope"
    primary_keys = ["scope"]
    replication_key = "scope"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("scope", StringType),


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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params


class GroupsPickerStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-groups/#api-rest-api-3-groups-picker-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    issue_out: issue out value
    """

    name = "groups_picker"
    path = "/groups/picker"
    primary_keys = ["groupId"]
    replication_key = "groupId"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("name", StringType),
        Property("html", StringType),
        Property("labels", ArrayType(StringType)),
        Property("groupId", StringType),


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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        resp_json = response.json()

        if isinstance(resp_json, list):
            results = resp_json
        elif resp_json.get("groups") is not None:
            results = resp_json["groups"]
        else:
            results = resp_json

        yield from results


class LicenseStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-license-metrics/#api-rest-api-3-instance-license-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    issue_out: issue out value
    """

    name = "license"
    path = "/instance/license"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("id", StringType),
        Property("plan", StringType),


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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        resp_json = response.json()

        if isinstance(resp_json, list):
            results = resp_json
        elif resp_json.get("applications") is not None:
            results = resp_json["applications"]
        else:
            results = resp_json

        yield from results


class ScreensStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-screens/#api-rest-api-3-screens-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    issue_out: issue out value
    """

    name = "screens"
    path = "/screens"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("id", IntegerType),
        Property("name", StringType),
        Property("description", StringType),


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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
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


class ScreenSchemesStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-screen-tab-fields/#api-rest-api-3-screens-screenid-tabs-tabid-fields-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    issue_out: issue out value
    """

    name = "screen_schemes"
    path = "/screenscheme"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("id", IntegerType),
        Property("name", StringType),
        Property("description", StringType),
        Property(
            "screens",
            ObjectType(
                Property("default", IntegerType),
            ),
        ),
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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
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


class StatusesSearchStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-screen-tab-fields/#api-rest-api-3-screens-screenid-tabs-tabid-fields-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    issue_out: issue out value
    """

    name = "statuses_search"
    path = "/statuses/search"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("id", StringType),
        Property("name", StringType),
        Property("statusCategory", StringType),
        Property(
            "scope",
            ObjectType(
                Property("type", StringType)
            ),
        ),
        Property("description", StringType),
        Property("usages", ArrayType(StringType)),
        Property("workflowUsages", ArrayType(StringType)),


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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
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


class WorkflowStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-workflows/#api-rest-api-3-workflow-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    issue_out: issue out value
    """

    name = "workflow"
    path = "/workflow"
    primary_keys = ["name"]
    replication_key = "lastModifiedDate"
    replication_method = "incremental"

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
                Property("type", StringType)
            ),
        ),
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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params


class WorkflowSearchStream(JiraStream):

    """
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-workflows/#api-rest-api-3-workflow-get
    """

    """
    columns: columns which will be added to fields parameter in api
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    issue_out: issue out value
    """

    name = "workflow_search"
    path = "/workflow/search"
    primary_keys = ["id"]
    replication_key = "updated"
    replication_method = "incremental"

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
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
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






























