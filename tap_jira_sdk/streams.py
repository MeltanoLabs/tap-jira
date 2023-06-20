"""Stream type classes for tap-jira-sdk."""

from __future__ import annotations

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_jira_sdk.client import JiraStream

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
    #replication_key = "accountId"
    #replication_method = "incremental"

    schema = PropertiesList(
        Property("self", StringType),
        Property("accountId", StringType),
        Property("accountType", StringType),
        Property("name", StringType),
        Property("emailAddress", StringType),
        Property("avatarUrls", StringType),
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
    #replication_key = "LastModifiedDate"
    #replication_method = "incremental"

    schema = PropertiesList(
        Property("id", StringType),
        Property("key", StringType),
        Property("name", StringType),
        Property("untranslatedName", StringType),
        Property("custom", BooleanType),
        Property("orderable", BooleanType),
        Property("navigable", BooleanType),
        Property("searchable", BooleanType),
        Property("clauseNames", StringType),
        Property("schema", StringType),

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

    name = "serverInfo"
    path = "/serverInfo"
    primary_keys = ["baseUrl"]
    #replication_key = "serverTime"
    #replication_method = "incremental"

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
        Property("defaultLocale", StringType),

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

    name = "issuetype"
    path = "/issuetype"
    primary_keys = ["id"]
    #replication_key = "self"
    #replication_method = "incremental"

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
    #replication_key = "self"
    #replication_method = "incremental"

    schema = PropertiesList(
        Property("self", StringType),
        Property("description", StringType),
        Property("iconUrl", StringType),
        Property("name", StringType),
        Property("untranslatedName", StringType),
        Property("id", StringType),
        Property("statusCategory", StringType),
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
    #replication_key = "self"
    #replication_method = "incremental"

    schema = PropertiesList(
        Property("expand", StringType),
        Property("self", StringType),
        Property("id", StringType),
        Property("key", StringType),
        Property("name", StringType),
        Property("avatarUrls", StringType),
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


class IssueOut1Stream(JiraStream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-1"

    name = "issueout1"
    path = "/issue/{}".format(issues_out)
    primary_keys = ["id"]
    replication_key = "updated"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("statuscategorychangedate", StringType),
        Property("issuetype", StringType),
        Property("timespent", StringType),
        Property("customfield_10030", StringType),
        Property("customfield_10031", StringType),
        Property("project", StringType),
        Property("customfield_10032", ArrayType(StringType)),
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
        Property("watches", StringType),
        Property("issuerestriction", StringType),
        Property("lastViewed", StringType),
        Property("created", StringType),
        Property("customfield_10020", StringType),
        Property("customfield_10021", StringType),
        Property("customfield_10022", StringType),
        Property("customfield_10023", StringType),
        Property("priority", StringType),
        Property("customfield_10024", StringType),
        Property("customfield_10025", StringType),
        Property("labels", ArrayType(StringType)),
        Property("customfield_10016", StringType),
        Property("customfield_10017", StringType),
        Property("customfield_10018", StringType),
        Property("customfield_10019", StringType),
        Property("timeestimate", StringType),
        Property("aggregatetimeoriginalestimate", StringType),
        Property("versions", ArrayType(StringType)),
        Property("issuelinks", ArrayType(StringType)),
        Property("assignee", StringType),
        Property("updated", StringType),
        Property("status", StringType),
        Property("components", ArrayType(StringType)),
        Property("timeoriginalestimate", StringType),
        Property("description", StringType),
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
        Property("creator", StringType),
        Property("subtasks", ArrayType(StringType)),
        Property("customfield_10041", StringType),
        Property("reporter", StringType),
        Property("customfield_10043", StringType),
        Property("customfield_10044", StringType),
        Property("aggregateprogress", StringType),
        Property("customfield_10045", StringType),
        Property("customfield_10001", StringType),
        Property("customfield_10002", StringType),
        Property("customfield_10003", StringType),
        Property("customfield_10004", StringType),
        Property("customfield_10038", StringType),
        Property("customfield_10039", StringType),
        Property("environment", StringType),
        Property("duedate", StringType),
        Property("progress", StringType),
        Property("comment", StringType),
        Property("votes", StringType),
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


class IssueOut4Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-4"

    name = "issueout4"
    path = "/issue/{}".format(issues_out)

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


class IssueOut5Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-5"

    name = "issueout5"
    path = "/issue/{}".format(issues_out)

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


class IssueOut6Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-6"

    name = "issueout6"
    path = "/issue/{}".format(issues_out)

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
    

class IssueOut8Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-8"

    name = "issueout8"
    path = "/issue/{}".format(issues_out)

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


class IssueOut9Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-9"

    name = "issueout9"
    path = "/issue/{}".format(issues_out)

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


class IssueOut10Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-10"

    name = "issueout10"
    path = "/issue/{}".format(issues_out)

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


class IssueOut11Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-11"

    name = "issuesout11"
    path = "/issue/{}".format(issues_out)

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


class IssueOut12Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-12"

    name = "issueout12"
    path = "/issue/{}".format(issues_out)

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
    

class IssueOut14Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-14"

    name = "issueout14"
    path = "/issue/{}".format(issues_out)

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


class IssueOut15Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-15"

    name = "issueout15"
    path = "/issue/{}".format(issues_out)

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


class IssueOut17Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-17"

    name = "issueout17"
    path = "/issue/{}".format(issues_out)

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


class IssueOut18Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-18"

    name = "issueout18"
    path = "/issue/{}".format(issues_out)

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


class IssueOut19Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-19"

    name = "issueout19"
    path = "/issue/{}".format(issues_out)

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


class IssueOut20Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-20"

    name = "issueout20"
    path = "/issue/{}".format(issues_out)

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


class IssueOut21Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-21"

    name = "issueout21"
    path = "/issue/{}".format(issues_out)

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


class IssueOut22Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-22"

    name = "issueout22"
    path = "/issue/{}".format(issues_out)

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


class IssueOut23Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-23"

    name = "issueout23"
    path = "/issue/{}".format(issues_out)

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


class IssueOut24Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-24"

    name = "issueout24"
    path = "/issue/{}".format(issues_out)

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


class IssueOut25Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-25"

    name = "issueout25"
    path = "/issue/{}".format(issues_out)

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


class IssueOut26Stream(IssueOut1Stream):

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
    issues_out: issue out value
    """

    issues_out = "OUT-26"

    name = "issue"
    path = "/issue/{}".format(issues_out)

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

    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        """
        We have out values from OUT-1 to OUT-26, we have records for each out value
        We can get records for each out value in a child class and then we can join them with get records function
        """
        issue_out1 = IssueOut1Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out4 = IssueOut4Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out5 = IssueOut5Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out6 = IssueOut6Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out8 = IssueOut8Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out9 = IssueOut9Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out10 = IssueOut10Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out11 = IssueOut11Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out12 = IssueOut12Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out14 = IssueOut14Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out15 = IssueOut15Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out17 = IssueOut17Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out18 = IssueOut18Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out19 = IssueOut19Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out20 = IssueOut20Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out21 = IssueOut21Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out22 = IssueOut22Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out23 = IssueOut23Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out24 = IssueOut24Stream(
            self._tap, schema={"properties": {}}
        )
        issue_out25 = IssueOut25Stream(
            self._tap, schema={"properties": {}}
        )
        issueout_records = list(issue_out1.get_records(context)) + list(issue_out4.get_records(context)) + list(issue_out5.get_records(context)) + list(issue_out6.get_records(context)) + list(issue_out8.get_records(context)) + list(issue_out9.get_records(context))+ list(issue_out10.get_records(context)) + list(issue_out11.get_records(context)) + list(issue_out12.get_records(context)) + list(issue_out14.get_records(context)) + list(issue_out15.get_records(context)) + list(issue_out17.get_records(context)) + list(issue_out18.get_records(context)) + list(issue_out19.get_records(context)) + list(issue_out20.get_records(context)) + list(issue_out21.get_records(context)) + list(issue_out22.get_records(context)) + list(issue_out23.get_records(context)) + list(issue_out24.get_records(context)) + list(issue_out25.get_records(context)) + list(super().get_records(context))
            
        return issueout_records                                                
    
    
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
        Property("fields", StringType),
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
    #replication_key = "self"
    #replication_method = "incremental"

    schema = PropertiesList(
        Property("permissions", StringType),

    ).to_dict()

    @property
    def url_base(self) -> str:
        version = self.config.get("api_version_3", "")
        base_url = "https://ryan-miranda.atlassian.net:443/rest/api/{}".format(version)
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

    name = "projectrole"
    path = "/role"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("self", StringType),
        Property("name", StringType),
        Property("id", IntegerType),
        Property("description", StringType),
        Property("scope", StringType),
        Property("actors", ArrayType(StringType)),

    ).to_dict()

    @property
    def url_base(self) -> str:
        version = self.config.get("api_version_3", "")
        base_url = "https://ryan-miranda.atlassian.net:443/rest/api/{}".format(version)
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

    @property
    def url_base(self) -> str:
        version = self.config.get("api_version_3", "")
        base_url = "https://ryan-miranda.atlassian.net:443/rest/api/{}".format(version)
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

    name = "permissionholder"
    path = "/permissionscheme"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("id", IntegerType),
        Property("self", StringType),
        Property("holder", StringType),
        Property("permission", StringType),

    ).to_dict()

    @property
    def url_base(self) -> str:
        version = self.config.get("api_version_3", "")
        base_url = "https://ryan-miranda.atlassian.net:443/rest/api/{}".format(version)
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
    path = "/sprint"
    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "incremental"

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
        version = self.config.get("agile_version", "")
        board_id = self.config.get("board_id", "")
        base_url = "https://ryan-miranda.atlassian.net:443/rest/agile/{}/board/{}".format(version, board_id)
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


class UserGroupJiraSoftwareStream(JiraStream):

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
    
    group_name = "jira-software-users"
    name = "usergroupjirasoftware"
    path = "/group/member?groupname={}".format(group_name)
    #primary_keys = ["user_id"]
    replication_key = "user_id"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("self", StringType),
        Property("user_id", StringType),
        Property("avatarUrls", StringType),
        Property("displayName", StringType),
        Property("active", BooleanType),
        Property("timeZone", StringType),
        Property("accountType", StringType),
        Property("group_name", StringType),

    ).to_dict()

    @property
    def url_base(self) -> str:
        version = self.config.get("api_version_3", "")
        base_url = "https://ryan-miranda.atlassian.net:443/rest/api/{}".format(version)
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
            row["group_name"] = self.group_name
            row["user_id"] = row["accountId"]
        except:
            pass
        
        return super().post_process(row, context)
    

class UserGroupConfluenceStream(UserGroupJiraSoftwareStream):

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
    
    group_name = "confluence-users"
    name = "usergroupconfluence"
    path = "/group/member?groupname={}".format(group_name)

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        """
        We can add a group name column with group name variable and a user id column  with account id column
        """

        try:
            row["group_name"] = self.group_name
            row["user_id"] = row["accountId"]
        except:
            pass
        
        return super().post_process(row, context)
    

class UserGroupSiteAdminsStream(UserGroupJiraSoftwareStream):

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
    
    group_name = "site-admins"
    name = "usergroupsiteadmins"
    path = "/group/member?groupname={}".format(group_name)

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        """
        We can add a group name column with group name variable and a user id column  with account id column
        """

        try:
            row["group_name"] = self.group_name
            row["user_id"] = row["accountId"]
        except:
            pass
        
        return super().post_process(row, context)
    

class UserGroupTrustedStream(UserGroupJiraSoftwareStream):

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
    
    group_name = "trusted-users-c10b9164-2085-42b7-96c3-2ec6c1102bad"
    name = "usergroup"
    path = "/group/member?groupname={}".format(group_name)

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        """
        We can add a group name column with group name variable and a user id column  with account id column
        """

        try:
            row["group_name"] = self.group_name
            row["user_id"] = row["accountId"]
        except:
            pass
        
        return super().post_process(row, context)
    
    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        """
        We can get records for each group value in a child class and then we can join them with get records function
        """
        jira_software = UserGroupJiraSoftwareStream(
            self._tap, schema={"properties": {}}
        )
        confluence = UserGroupConfluenceStream(
            self._tap, schema={"properties": {}}
        )
        site_admin = UserGroupSiteAdminsStream(
            self._tap, schema={"properties": {}}
        )
        jira_records = list(jira_software.get_records(context)) + list(confluence.get_records(context)) + list(site_admin.get_records(context)) + list(super().get_records(context))
            
        return jira_records


class ProjectRoleAdminActorStream(JiraStream):

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
    
    name = "projectroleadminactor"
    path = None

    primary_keys = ["id"]
    replication_key = "id"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("self", StringType),
        Property("name", StringType),
        Property("id", StringType),
        Property("description", StringType),
        Property("actors", StringType),
        Property("scope", StringType),

    ).to_dict()

    @property
    def url_base(self) -> str:
        version = self.config.get("api_version_3", "")
        project_id = self.config.get("project_id", "")
        admin = self.config.get("role_admin_id", "")
        base_url = "https://ryan-miranda.atlassian.net:443/rest/api/{}/project/{}/role/{}".format(version, project_id, admin)
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
    

class ProjectRoleViewerActorStream(ProjectRoleAdminActorStream):

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
    
    name = "projectrolevieweractor"
    path = None

    schema = PropertiesList(
        Property("self", StringType),
        Property("name", StringType),
        Property("id", StringType),
        Property("description", StringType),
        Property("actors", StringType),
        Property("scope", StringType),

    ).to_dict()

    @property
    def url_base(self) -> str:
        version = self.config.get("api_version_3", "")
        project_id = self.config.get("project_id", "")
        viewer = self.config.get("role_viewer_id", "")
        base_url = "https://ryan-miranda.atlassian.net:443/rest/api/{}/project/{}/role/{}".format(version, project_id, viewer)
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


class ProjectRoleMemberActorStream(ProjectRoleAdminActorStream):

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
    
    name = "projectrolememberactor"
    path = None

    schema = PropertiesList(
        Property("self", StringType),
        Property("name", StringType),
        Property("id", StringType),
        Property("description", StringType),
        Property("actors", StringType),
        Property("scope", StringType),

    ).to_dict()

    @property
    def url_base(self) -> str:
        version = self.config.get("api_version_3", "")
        project_id = self.config.get("project_id", "")
        member = self.config.get("role_member_id", "")
        base_url = "https://ryan-miranda.atlassian.net:443/rest/api/{}/project/{}/role/{}".format(version, project_id, member)
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


class ProjectRoleAtlassianActorStream(ProjectRoleAdminActorStream):

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
    
    name = "projectroleactor"
    path = None

    schema = PropertiesList(
        Property("self", StringType),
        Property("name", StringType),
        Property("id", IntegerType),
        Property("description", StringType),
        Property("actors", ArrayType(StringType)),
        Property("scope", StringType),

    ).to_dict()

    @property
    def url_base(self) -> str:
        version = self.config.get("api_version_3", "")
        project_id = self.config.get("project_id", "")
        atlassian = self.config.get("role_altasian_id", "")
        base_url = "https://ryan-miranda.atlassian.net:443/rest/api/{}/project/{}/role/{}".format(version, project_id, atlassian)
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
    
    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        """
        We have records for each role actor
        We can get records for each role actor in a child class and then we can join them with get records function
        """
        admin = ProjectRoleAdminActorStream(
            self._tap, schema={"properties": {}}
        )
        viewer = ProjectRoleViewerActorStream(
            self._tap, schema={"properties": {}}
        )
        member = ProjectRoleMemberActorStream(
            self._tap, schema={"properties": {}}
        )
        role_records = list(admin.get_records(context)) + list(viewer.get_records(context)) + list(member.get_records(context)) + list(super().get_records(context))
            
        return role_records
    

class IssueOut1WatcherStream(JiraStream):

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

    issues_out = "OUT-1"

    name = "issueout1watcher"
    path = "/issue/{}/watchers".format(issues_out)
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


class IssueOut4WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-4"

    name = "issueout4watcher"
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


class IssueOut5WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-5"

    name = "issueout5watcher"
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


class IssueOut6WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-6"

    name = "issueout6watcher"
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
    

class IssueOut8WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-8"

    name = "issueout8watcher"
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


class IssueOut9WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-9"

    name = "issueout9watcher"
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


class IssueOut10WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-10"

    name = "issueout10watcher"
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


class IssueOut11WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-11"

    name = "issueout11watcher"
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


class IssueOut12WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-12"

    name = "issueout12watcher"
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
    

class IssueOut14WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-14"

    name = "issueout14watcher"
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


class IssueOut15WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-15"

    name = "issueout15watcher"
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


class IssueOut17WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-17"

    name = "issueout17watcher"
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


class IssueOut18WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-18"

    name = "issueout18watcher"
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


class IssueOut19WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-19"

    name = "issueout19watcher"
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


class IssueOut20WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-20"

    name = "issueout20watcher"
    path = "/issue/{}/watchers".format(issues_out)

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        """
        We can add a key column which have out value
        We can get the user id column from watchers column
        """

        try:
            row["key"] = self.issues_out
            row["id"] = row["user_id"] = row.get("watchers")[0].get("accountId")
        except:
            pass
        
        return super().post_process(row, context)


class IssueOut21WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-21"

    name = "issueout21watcher"
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


class IssueOut22WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-22"

    name = "issueout22watcher"
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


class IssueOut23WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-23"

    name = "issueout23watcher"
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


class IssueOut24WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-24"

    name = "issueout24watcher"
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


class IssueOut25WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-25"

    name = "issueout25watcher"
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


class IssueOut26WatcherStream(IssueOut1WatcherStream):

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

    issues_out = "OUT-26"

    name = "issuewatcher"
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

    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        """
        We have out values from OUT-1 to OUT-26, we have records for each out value
        We can get records for each out value in a child class and then we can join them with get records function
        """
        issue_out1 = IssueOut1WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out4 = IssueOut4WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out5 = IssueOut5WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out6 = IssueOut6WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out8 = IssueOut8WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out9 = IssueOut9WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out10 = IssueOut10WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out11 = IssueOut11WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out12 = IssueOut12WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out14 = IssueOut14WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out15 = IssueOut15WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out17 = IssueOut17WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out18 = IssueOut18WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out19 = IssueOut19WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out20 = IssueOut20WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out21 = IssueOut21WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out22 = IssueOut22WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out23 = IssueOut23WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out24 = IssueOut24WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issue_out25 = IssueOut25WatcherStream(
            self._tap, schema={"properties": {}}
        )
        issuewatcher_records = list(issue_out1.get_records(context)) + list(issue_out4.get_records(context)) + list(issue_out5.get_records(context)) + list(issue_out6.get_records(context)) + list(issue_out8.get_records(context)) + list(issue_out9.get_records(context))+ list(issue_out10.get_records(context)) + list(issue_out11.get_records(context)) + list(issue_out12.get_records(context)) + list(issue_out14.get_records(context)) + list(issue_out15.get_records(context)) + list(issue_out17.get_records(context)) + list(issue_out18.get_records(context)) + list(issue_out19.get_records(context)) + list(issue_out20.get_records(context)) + list(issue_out21.get_records(context)) + list(issue_out22.get_records(context)) + list(issue_out23.get_records(context)) + list(issue_out24.get_records(context)) + list(issue_out25.get_records(context)) + list(super().get_records(context))
            
        return issuewatcher_records    
    

class IssueKeyWatcherStream(JiraStream):

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

    name = "issuekeywatcher"
    path = "/watchers"
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

    @property
    def url_base(self) -> str:
        """
        Returns base url
        """
        version = self.config.get("api_version_2", "")
        self.issues_out = self.config.get("jira_issue_keys", "").split(",")[0]
        base_url = "https://ryan-miranda.atlassian.net:443/rest/api/{}/issue/{}".format(version, self.issues_out)
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
    
    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        """
        We have out values from OUT-1 to OUT-26, we have records for each out value
        We can get records for each out value in a child class and then we can join them with get records function
        """

        jira_keys = self.config.get("jira_issue_keys", "").split(",")
        
        """
        issue_key_records_list = []
     
        for i in (jira_keys):
            issue_key = type('IssueKey'+i+'Stream', (IssueKeyWatcherStream,), {"issues_out": i, "name": "issuewatcher"})
            issue_key_stream = issue_key(
                self._tap, schema={"properties": {}}    
            )
            issuekey_records = list(issue_key_stream.get_records(context))
            issue_key_records_list.append(issuekey_records)
        """
            
        return issuekey_records
    
    
    
       
    
    