"""Stream type classes for tap-jira-sdk."""

from __future__ import annotations

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_jira_sdk.client import JiraStream

PropertiesList = th.PropertiesList
Property = th.Property
ObjectType = th.ObjectType
DateTimeType = th.DateTimeType
StringType = th.StringType
ArrayType = th.ArrayType
BooleanType = th.BooleanType
IntegerType = th.IntegerType

class UsersStream(JiraStream):

    columns = """
                 self, accountId, accountType, avatarUrls, displayName, active, timeZone, locale, groups, applicationRoles, expand
              """

    name = "user"
    path = "/user?accountId=62851352222d36006fb739dc"
    primary_keys = ["accountId"]
    #replication_key = "accountId"
    #replication_method = "incremental"

    schema = PropertiesList(
        Property("self", StringType),
        Property("accountId", StringType),
        Property("accountType", StringType),
        Property("avatarUrls", StringType),
        Property("displayName", StringType),
        Property("active", StringType),
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
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params


class FieldStream(JiraStream):

    columns = """
                 id, key, name, untranslatedName, custom, orderable, navigate, searchable, clauseNames, schema, array
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
        Property("untranslatedname", StringType),
        Property("custom", StringType),
        Property("array", StringType),
        Property("orderable", StringType),
        Property("navigate", StringType),
        Property("searchable", StringType),
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
        Property("versionNumbers", StringType),
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

    columns = """
                 self, id, description, iconUrl, name, untranslatedName, subtask, avatarId, hierarchyLevel, scope
              """

    name = "IssueType"
    path = "/issuetype"
    primary_keys = ["id"]
    #replication_key = "self"
    #replication_method = "incremental"

    schema = PropertiesList(
        Property("self", StringType),
        Property("id", IntegerType),
        Property("description", StringType),
        Property("iconUrl", StringType),
        Property("name", StringType),
        Property("untranslatedName", StringType),
        Property("subtask", StringType),
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
    """Define custom stream."""

    columns = """
                 self, description, iconUrl, name, untranslatedName, id, statusCategory, scope
              """

    name = "Status"
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
        Property("id", IntegerType),
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

    columns = """
                 expand, self, id, key, name, avatarUrls, projectTypeKey, simplified, style, isPrivate, properties, entityId, uuid
              """

    name = "Project"
    path = "/project"
    primary_keys = ["id"]
    #replication_key = "self"
    #replication_method = "incremental"

    schema = PropertiesList(
        Property("expand", StringType),
        Property("self", StringType),
        Property("id", IntegerType),
        Property("key", StringType),
        Property("name", StringType),
        Property("avatarUrls", StringType),
        Property("projectTypeKey", StringType),
        Property("simplified", StringType),
        Property("style", StringType),
        Property("isPrivate", StringType),
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

    columns = """
                 expand, id, self, key, fields
              """

    name = "Issue"
    path = "2/issue/OUT-17"
    primary_keys = ["id"]
    #replication_key = "self"
    #replication_method = "incremental"

    schema = PropertiesList(
        Property("expand", StringType),
        Property("id", IntegerType),
        Property("self", StringType),
        Property("key", StringType),
        Property("fields", StringType),

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
    
    
class SearchStream(JiraStream):

    name = "Search"
    path = "/search"
    primary_keys = ["id"]
    replication_key = "updated"
    replication_method = "incremental"

    schema = PropertiesList(
        Property("expand", StringType),
        Property("id", IntegerType),
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

        try:
            row["created"] = row.get("fields").get("created")
            row["updated"] = row.get("fields").get("updated")
        except:
            pass
        
        return super().post_process(row, context)


class PermissionStream(JiraStream):

    columns = """
                 permissions
              """

    name = "Permission"
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
        Property("id", IntegerType),

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
        Property("originBoardId", StringType),
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
        Property("active", StringType),
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

        try:
            row["group_name"] = self.group_name
            row["user_id"] = row["accountId"]
        except:
            pass
        
        return super().post_process(row, context)
    

class UserGroupConfluenceStream(UserGroupJiraSoftwareStream):
    
    group_name = "confluence-users"
    name = "usergroupconfluence"
    path = "/group/member?groupname={}".format(group_name)

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:

        try:
            row["group_name"] = self.group_name
            row["user_id"] = row["accountId"]
        except:
            pass
        
        return super().post_process(row, context)
    

class UserGroupSiteAdminsStream(UserGroupJiraSoftwareStream):
    
    group_name = "site-admins"
    name = "usergroupsiteadmins"
    path = "/group/member?groupname={}".format(group_name)

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:

        try:
            row["group_name"] = self.group_name
            row["user_id"] = row["accountId"]
        except:
            pass
        
        return super().post_process(row, context)
    

class UserGroupTrustedStream(UserGroupJiraSoftwareStream):
    
    group_name = "trusted-users-c10b9164-2085-42b7-96c3-2ec6c1102bad"
    name = "usergroup"
    path = "/group/member?groupname={}".format(group_name)

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:

        try:
            row["group_name"] = self.group_name
            row["user_id"] = row["accountId"]
        except:
            pass
        
        return super().post_process(row, context)
    
    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
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
    

    
    
        
       
    
    