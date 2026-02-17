"""Stream type classes for Jira Service Management (JSM) used in tap-jira.

This module defines stream classes for extracting data from the Jira Service
Management REST API. These streams use the `/rest/servicedeskapi` endpoints
and support the following hierarchy:

    OrganizationStream (top-level)
        └── Organizations that can be associated with service desks

    ServiceDeskStream (top-level)
        ├── ServiceDeskCustomerStream (child)
        │       └── Customers associated with a service desk
        ├── ServiceDeskQueuesStream (child)
        │       └── Issue queues configured for a service desk
        ├── ServiceDeskRequestTypeStream (child)
        │       └── Request types available in a service desk
        │           └── ServiceDeskRequestTypeFieldStream (grandchild)
        │                   └── Fields for each request type
        ├── ServiceDeskRequestTypeGroupStream (child)
        │       └── Groupings of request types
        └── ServiceDeskKnowledgebaseArticleStream (child)
                └── Knowledgebase articles for a service desk

    RequestStream (top-level)
        ├── RequestApprovalStream (child)
        │       └── Approvals associated with a request
        ├── RequestAttachmentStream (child)
        │       └── Attachments on a request
        ├── RequestCommentStream (child)
        │       └── Comments on a request
        ├── RequestParticipantStream (child)
        │       └── Participants on a request
        ├── RequestSlaStream (child)
        │       └── SLA information for a request
        └── RequestStatusStream (child)
                └── Status history for a request

All child streams inherit context from their parent stream (servicedesk_id)
and use post_process() to include the parent ID in each record.
"""

import sys

from tap_jira.client import JiraServiceManagementStream, JiraServiceManagementPaginatedStream
from tap_jira.streams import PropertiesList

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

from singer_sdk.helpers.types import Context, Record


from singer_sdk import typing as th  # JSON Schema typing helpers

Property = th.Property
ObjectType = th.ObjectType
DateTimeType = th.DateTimeType
DateType = th.DateType
StringType = th.StringType
ArrayType = th.ArrayType
BooleanType = th.BooleanType
IntegerType = th.IntegerType
NumberType = th.NumberType

# Reusable schema for JSM icon objects containing multiple resolution URLs.
IconType = ObjectType(
    Property("id", StringType),
    Property("_links", ObjectType(
        Property("iconUrls", ObjectType(
            Property("16x16", StringType),
            Property("24x24", StringType),
            Property("32x32", StringType),
            Property("64x64", StringType),
        ))
    ))
)

class OrganizationStream(JiraServiceManagementPaginatedStream):
    """Stream for JSM organizations.

    Organizations in JSM are groups of customers that can be associated with
    service desks. They allow managing customer access and grouping related
    customers together.

    API Reference:
        https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-organization/#api-rest-servicedeskapi-organization-get
    """

    name = "organization"
    path = "/organization"
    primary_keys = ("id",)
    records_jsonpath = "$.values[*]"

    schema = PropertiesList(
        Property("id", StringType, required=True),
        Property("name", StringType),
        Property("uuid", StringType),
        Property("scimManaged", BooleanType),
    ).to_dict()

class ServiceDeskStream(JiraServiceManagementPaginatedStream):
    """Stream for JSM service desks.

    Service desks are the primary entity in JSM, representing a customer-facing
    help desk or support portal. Each service desk is linked to a Jira project
    and provides the parent context for customers, queues, and request types.

    This stream serves as the parent for multiple child streams that require
    a servicedesk_id in their path.

    API Reference:
        https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-servicedesk/#api-rest-servicedeskapi-servicedesk-get
    """

    name = "servicedesk"
    path = "/servicedesk"
    primary_keys = ("id",)
    records_jsonpath = "$.values[*]"    

    schema = PropertiesList(
        Property("id", StringType, required=True),
        Property("projectId", StringType),
        Property("projectKey", StringType),
        Property("projectName", StringType),
        Property("projectTypeKey", StringType),
    ).to_dict()

    @override
    def get_child_context(self, record: Record, context: Context | None) -> Context:
        """Return a context dictionary for child streams."""
        return {"servicedesk_id": record["id"]}

class ServiceDeskCustomerStream(JiraServiceManagementPaginatedStream):
    """Stream for customers associated with a service desk.

    Customers are users who can raise requests in a service desk. This stream
    extracts customer information for each service desk, including their
    account details and contact information.

    Note: This endpoint requires the X-ExperimentalApi header to be set.

    Parent: ServiceDeskStream (provides servicedesk_id context)

    API Reference:
        https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-servicedesk/#api-rest-servicedeskapi-servicedesk-servicedeskid-customer-get
    """

    name = "customer"
    path = "/servicedesk/{servicedesk_id}/customer"
    primary_keys = ("accountId", "servicedeskId")
    records_jsonpath = "$.values[*]"
    parent_stream_type = ServiceDeskStream

    schema = PropertiesList(
        Property("servicedeskId", StringType),
        Property("accountId", StringType, required=True),
        Property("active", BooleanType),
        Property("displayName", StringType),
        Property("emailAddress", StringType),
        Property("key", StringType),
        Property("name", StringType),
        Property("timezone", StringType),
    ).to_dict()

    @override
    def post_process(
        self,
        row: Record,
        context: Context | None = None,
    ) -> Record | None:
        """Post-process the record before it is returned."""
        if context:
            row["servicedeskId"] = context["servicedesk_id"]
        return row

    @override
    def prepare_request(self, context, next_page_token):
        prepared_request = super().prepare_request(context, next_page_token)

        prepared_request.headers["X-ExperimentalApi"] = "opt-in"
        return prepared_request


class ServiceDeskQueuesStream(JiraServiceManagementPaginatedStream):
    """Stream for issue queues in a service desk.

    Queues are filtered views of issues in a service desk, defined by JQL
    queries. Agents use queues to organize and prioritize their work. Each
    queue includes its JQL filter, issue count, and configured display fields.

    Parent: ServiceDeskStream (provides servicedesk_id context)

    API Reference:
        https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-servicedesk/#api-rest-servicedeskapi-servicedesk-servicedeskid-queue-get
    """

    name = "queue"
    path = "/servicedesk/{servicedesk_id}/queue"
    primary_keys = ("id", "servicedeskId")
    records_jsonpath = "$.values[*]"
    parent_stream_type = ServiceDeskStream


    schema = PropertiesList(
        Property("servicedeskId", StringType),
        Property("id", StringType, required=True),
        Property("issueCount", IntegerType),
        Property("jql", StringType),
        Property("name", StringType),
        Property("fields", ArrayType(StringType)),
    ).to_dict()

    @override
    def post_process(
        self,
        row: Record,
        context: Context | None = None,
    ) -> Record | None:
        """Post-process the record before it is returned."""
        if context:
            row["servicedeskId"] = context["servicedesk_id"]
        return row

class ServiceDeskRequestTypeStream(JiraServiceManagementPaginatedStream):
    """Stream for request types available in a service desk.

    Request types define the kinds of requests customers can submit through
    the service desk portal. Each request type maps to a Jira issue type and
    includes configuration for help text, icons, and field visibility.

    This stream serves as the parent for ServiceDeskRequestTypeFieldStream.

    Parent: ServiceDeskStream (provides servicedesk_id context)

    API Reference:
        https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-servicedesk/#api-rest-servicedeskapi-servicedesk-servicedeskid-requesttype-get
    """

    name = "requesttype"
    path = "/servicedesk/{servicedesk_id}/requesttype"
    primary_keys = ("id",)
    records_jsonpath = "$.values[*]"
    parent_stream_type = ServiceDeskStream

    schema = PropertiesList(
        Property("servicedeskId", StringType),
        Property("id", StringType, required=True),
        Property("canCreateRequest", BooleanType),
        Property("description", StringType),
        Property("groupIds", ArrayType(StringType)),
        Property("helpText", StringType),
        Property("icon", IconType),
        Property("issueTypeId", StringType),
        Property("name", StringType),
        Property("portalId", StringType),
        Property("practice", StringType),
        Property("restrictionStatus", StringType),
        
    ).to_dict()

    @override
    def post_process(
        self,
        row: Record,
        context: Context | None = None,
    ) -> Record | None:
        """Post-process the record before it is returned."""
        if context:
            row["servicedeskId"] = context["servicedesk_id"]
        return row
    
    @override
    def get_child_context(self, record: Record, context: Context | None) -> Context:
        """Return a context dictionary for child streams."""
        return {
                "servicedesk_id": record["servicedeskId"],
                "requesttype_id": record["id"]
            }


# Schema for field value options in request type fields.
# Note: The JSM API defines this as potentially recursive (children property),
# but recursive types are not supported here.
RequestTypeFieldValueDTO = ObjectType(
    Property("label", StringType),
    Property("value", StringType),
)

class ServiceDeskRequestTypeFieldStream(JiraServiceManagementStream):
    """Stream for fields associated with a request type.

    Each request type has a set of fields that customers can fill in when
    creating a request. This stream extracts field metadata including
    visibility, required status, valid values, and default values.

    Note: This stream does not use pagination as the endpoint returns all
    fields for a request type in a single response.

    Parent: ServiceDeskRequestTypeStream (provides servicedesk_id and requesttype_id context)

    API Reference:
        https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-servicedesk/#api-rest-servicedeskapi-servicedesk-servicedeskid-requesttype-requesttypeid-field-get
    """

    name = "requesttypefield"
    path = "/servicedesk/{servicedesk_id}/requesttype/{requesttype_id}/field"
    primary_keys = ("servicedeskId","requesttypeId", "fieldId",)
    records_jsonpath = "$.requestTypeFields[*]"
    parent_stream_type = ServiceDeskRequestTypeStream

    schema = PropertiesList(
        Property("servicedeskId", StringType),
        Property("requesttypeId", StringType),

        Property("description", StringType),
        Property("fieldId", StringType, required=True),
        Property("name", StringType),
        Property("presentValues", ArrayType(StringType)),
        Property("required", BooleanType),
        Property("visible", BooleanType),

        Property("validValues", ArrayType(RequestTypeFieldValueDTO)),
        Property("defaultValues", ArrayType(RequestTypeFieldValueDTO)),

    ).to_dict()

    @override
    def post_process(
        self,
        row: Record,
        context: Context | None = None,
    ) -> Record | None:
        """Post-process the record before it is returned."""
        if context:
            row["servicedeskId"] = context["servicedesk_id"]
            row["requesttypeId"] = context["requesttype_id"]
        return row

class ServiceDeskRequestTypeGroupStream(JiraServiceManagementPaginatedStream):
    """Stream for request type groups in a service desk.

    Request type groups are used to organize request types in the customer
    portal. They provide logical groupings (e.g., "IT Help", "HR Requests")
    that help customers find the appropriate request type.

    Parent: ServiceDeskStream (provides servicedesk_id context)

    API Reference:
        https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-servicedesk/#api-rest-servicedeskapi-servicedesk-servicedeskid-requesttypegroup-get
    """

    name = "requesttypegroup"
    path = "/servicedesk/{servicedesk_id}/requesttypegroup"
    primary_keys = ("id","servicedeskId")
    records_jsonpath = "$.values[*]"
    parent_stream_type = ServiceDeskStream

    schema = PropertiesList(
        Property("servicedeskId", StringType),
        Property("id", StringType, required=True),
        Property("name", StringType),
    ).to_dict()

    @override
    def post_process(
        self,
        row: Record,
        context: Context | None = None,
    ) -> Record | None:
        """Post-process the record before it is returned."""
        if context:
            row["servicedeskId"] = context["servicedesk_id"]
        return row


# =============================================================================
# Knowledgebase Streams
# =============================================================================

# Reusable schema for article content containing iframe source URL.
ArticleContentType = ObjectType(
    Property("iframeSrc", StringType),
)

# Reusable schema for article source information.
ArticleSourceType = ObjectType(
    Property("type", StringType),
)


class ServiceDeskKnowledgebaseArticleStream(JiraServiceManagementPaginatedStream):
    """Stream for knowledgebase articles associated with a service desk.

    Knowledgebase articles provide self-service content for customers. This
    stream searches for articles linked to each service desk. The search query
    can be configured via `stream_options.knowledgebase.query` in the tap config.

    Note: This endpoint requires the X-ExperimentalApi header and a query
    parameter. By default, searches for all articles using a wildcard query.

    Parent: ServiceDeskStream (provides servicedesk_id context)

    API Reference:
        https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-knowledgebase/#api-rest-servicedeskapi-servicedesk-servicedeskid-knowledgebase-article-get
    """

    name = "knowledgebase_article"
    path = "/servicedesk/{servicedesk_id}/knowledgebase/article"
    primary_keys = ("servicedeskId", "title",)
    records_jsonpath = "$.values[*]"
    parent_stream_type = ServiceDeskStream

    schema = PropertiesList(
        Property("servicedeskId", StringType),
        Property("title", StringType, required=True),
        Property("excerpt", StringType),
        Property("source", ArticleSourceType),
        Property("content", ArticleContentType),
    ).to_dict()

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: int | None,
    ) -> dict:
        """Return URL parameters including the required query parameter."""
        params = super().get_url_params(context, next_page_token)
        # Get query from config or use default wildcard
        query = (
            self.config
            .get("stream_options", {})
            .get("knowledgebase", {})
            .get("query", "*")
        )
        params["query"] = query
        params["highlight"] = "false"
        return params

    @override
    def prepare_request(self, context, next_page_token):
        """Add experimental API header to the request."""
        prepared_request = super().prepare_request(context, next_page_token)
        prepared_request.headers["X-ExperimentalApi"] = "opt-in"
        return prepared_request

    @override
    def validate_response(self, response) -> None:
        """Handle 404 for service desks without knowledgebase configured."""
        if response.status_code == 404:
            self.logger.warning(
                f"Knowledgebase not configured for {response.url}. Skipping."
            )
            return
        super().validate_response(response)

    @override
    def post_process(
        self,
        row: Record,
        context: Context | None = None,
    ) -> Record | None:
        """Post-process the record before it is returned."""
        if context:
            row["servicedeskId"] = context["servicedesk_id"]
        return row

# =============================================================================
# Request Streams
# =============================================================================

# Reusable schema for JSM date objects with multiple format representations.
JsmDateType = ObjectType(
    Property("epochMillis", IntegerType),
    Property("friendly", StringType),
    Property("iso8601", StringType),
    Property("jira", StringType),
)

# Reusable schema for JSM user objects in request responses.
RequestUserType = ObjectType(
    Property("accountId", StringType),
    Property("active", BooleanType),
    Property("displayName", StringType),
    Property("emailAddress", StringType),
    Property("key", StringType),
    Property("name", StringType),
    Property("timeZone", StringType),
)

# Reusable schema for request status information.
RequestStatusType = ObjectType(
    Property("status", StringType),
    Property("statusCategory", StringType),
    Property("statusDate", JsmDateType),
)

# Reusable schema for request field values.
RequestFieldValueType = ObjectType(
    Property("fieldId", StringType),
    Property("label", StringType),
    Property("value", StringType),
)


class RequestStream(JiraServiceManagementPaginatedStream):
    """Stream for JSM customer requests.

    Customer requests are the core entity in JSM, representing issues raised
    by customers through the service desk portal. This stream extracts all
    requests visible to the authenticated user.

    This stream serves as the parent for multiple child streams that require
    an issueIdOrKey in their path.

    Note on identifiers:
        Both issueId and issueKey are included in records and passed to child
        streams via context. Understanding when to use each:

        - issueId: Stable numeric identifier that never changes, even when an
          issue is moved between projects. Use for primary keys, foreign key
          relationships, and permanent external references.

        - issueKey: Human-readable identifier (e.g., PROJ-123) consisting of
          project key + sequential number. Changes when an issue moves to a
          different project. Use for display, debugging, and user-facing output.

        Child streams use issueId in API paths (via issue_id_or_key context)
        to ensure stability across syncs, even if issues are moved between
        projects.

    API Reference:
        https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-request/#api-rest-servicedeskapi-request-get
    """

    name = "request"
    path = "/request"
    primary_keys = ("issueId",)
    records_jsonpath = "$.values[*]"

    schema = PropertiesList(
        Property("issueId", StringType, required=True),
        Property("issueKey", StringType),
        Property("requestTypeId", StringType),
        Property("servicedeskId", StringType),
        Property("createdDate", JsmDateType),
        Property("reporter", RequestUserType),
        Property("currentStatus", RequestStatusType),
        Property("requestFieldValues", ArrayType(RequestFieldValueType)),
    ).to_dict()

    @override
    def get_child_context(self, record: Record, context: Context | None) -> Context:
        """Return a context dictionary for child streams."""
        return {
            "issue_key": record["issueKey"],
            "issue_id": record["issueId"],
            "issue_id_or_key": record["issueId"]
        }

# Schema for individual approvers within an approval.
ApproverType = ObjectType(
    Property("approver", RequestUserType),
    Property("approverDecision", StringType),
)


class RequestApprovalStream(JiraServiceManagementPaginatedStream):
    """Stream for approvals associated with a request.

    Approvals are used in JSM to require sign-off from designated approvers
    before a request can proceed. This stream extracts approval information
    including the approvers, their decisions, and the overall approval status.

    Parent: RequestStream (provides issue_id_or_key context)

    API Reference:
        https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-request/#api-rest-servicedeskapi-request-issueidorkey-approval-get
    """

    name = "request_approval"
    path = "/request/{issue_id_or_key}/approval"
    primary_keys = ("issueId", "id",)
    records_jsonpath = "$.values[*]"
    parent_stream_type = RequestStream

    schema = PropertiesList(
        Property("issueKey", StringType),
        Property("issueId", StringType),
        Property("id", StringType, required=True),
        Property("name", StringType),
        Property("finalDecision", StringType),
        Property("canAnswerApproval", BooleanType),
        Property("approvers", ArrayType(ApproverType)),
        Property("createdDate", JsmDateType),
        Property("completedDate", JsmDateType),
    ).to_dict()

    @override
    def post_process(
        self,
        row: Record,
        context: Context | None = None,
    ) -> Record | None:
        """Post-process the record before it is returned."""
        if context:
            row["issueKey"] = context.get("issue_key")
            row["issueId"] = context.get("issue_id")
        return row


class RequestAttachmentStream(JiraServiceManagementPaginatedStream):
    """Stream for attachments on a request.

    Attachments are files uploaded to a request by customers or agents.
    This stream extracts attachment metadata including filename, size,
    MIME type, and the user who created the attachment.

    Parent: RequestStream (provides issue_id_or_key context)

    API Reference:
        https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-request/#api-rest-servicedeskapi-request-issueidorkey-attachment-get
    """

    name = "request_attachment"
    path = "/request/{issue_id_or_key}/attachment"
    primary_keys = ("issueId", "filename")
    records_jsonpath = "$.values[*]"
    parent_stream_type = RequestStream

    schema = PropertiesList(
        Property("issueKey", StringType),
        Property("issueId", StringType),
        Property("filename", StringType, required=True),
        Property("author", RequestUserType),
        Property("created", JsmDateType),
        Property("size", IntegerType),
        Property("mimeType", StringType),
    ).to_dict()

    @override
    def post_process(
        self,
        row: Record,
        context: Context | None = None,
    ) -> Record | None:
        """Post-process the record before it is returned."""
        if context:
            row["issueKey"] = context.get("issue_key")
            row["issueId"] = context.get("issue_id")
        return row


class RequestCommentStream(JiraServiceManagementPaginatedStream):
    """Stream for comments on a request.

    Comments are messages added to a request by customers, agents, or the
    system. Comments can be public (visible to customers) or internal
    (visible only to agents).

    Parent: RequestStream (provides issue_id_or_key context)

    API Reference:
        https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-request/#api-rest-servicedeskapi-request-issueidorkey-comment-get
    """

    name = "request_comment"
    path = "/request/{issue_id_or_key}/comment"
    primary_keys = ("issueId", "id",)
    records_jsonpath = "$.values[*]"
    parent_stream_type = RequestStream

    schema = PropertiesList(
        Property("issueKey", StringType),
        Property("issueId", StringType),
        Property("id", StringType, required=True),
        Property("body", StringType),
        Property("renderedBody", ObjectType(
            Property("html", StringType),
        )),
        Property("public", BooleanType),
        Property("author", RequestUserType),
        Property("created", JsmDateType),
    ).to_dict()

    @override
    def post_process(
        self,
        row: Record,
        context: Context | None = None,
    ) -> Record | None:
        """Post-process the record before it is returned."""
        if context:
            row["issueKey"] = context.get("issue_key")
            row["issueId"] = context.get("issue_id")
        return row


class RequestParticipantStream(JiraServiceManagementPaginatedStream):
    """Stream for participants on a request.

    Participants are users who are involved in a request but are not the
    reporter. They can view and comment on the request through the portal.

    Parent: RequestStream (provides issue_id_or_key context)

    API Reference:
        https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-request/#api-rest-servicedeskapi-request-issueidorkey-participant-get
    """

    name = "request_participant"
    path = "/request/{issue_id_or_key}/participant"
    primary_keys = ("issueId", "accountId",)
    records_jsonpath = "$.values[*]"
    parent_stream_type = RequestStream

    schema = PropertiesList(
        Property("issueId", StringType),
        Property("issueKey", StringType),
        Property("accountId", StringType, required=True),
        Property("active", BooleanType),
        Property("displayName", StringType),
        Property("emailAddress", StringType),
        Property("key", StringType),
        Property("name", StringType),
        Property("timeZone", StringType),
    ).to_dict()

    @override
    def post_process(
        self,
        row: Record,
        context: Context | None = None,
    ) -> Record | None:
        """Post-process the record before it is returned."""
        if context:
            row["issueKey"] = context.get("issue_key")
            row["issueId"] = context.get("issue_id")
        return row


# Schema for SLA duration with friendly and millis representations.
DurationType = ObjectType(
    Property("friendly", StringType),
    Property("millis", IntegerType),
)

# Schema for an ongoing or completed SLA cycle.
SlaCycleType = ObjectType(
    Property("breached", BooleanType),
    Property("breachTime", JsmDateType),
    Property("elapsedTime", DurationType),
    Property("goalDuration", DurationType),
    Property("paused", BooleanType),
    Property("remainingTime", DurationType),
    Property("startTime", JsmDateType),
    Property("stopTime", JsmDateType),
    Property("withinCalendarHours", BooleanType),
)


class RequestSlaStream(JiraServiceManagementPaginatedStream):
    """Stream for SLA information associated with a request.

    SLAs (Service Level Agreements) track time-based metrics for requests,
    such as time to first response or time to resolution. This stream
    extracts SLA status including elapsed time, remaining time, and whether
    the SLA has been breached.

    Parent: RequestStream (provides issue_id_or_key context)

    API Reference:
        https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-request/#api-rest-servicedeskapi-request-issueidorkey-sla-get
    """

    name = "request_sla"
    path = "/request/{issue_id_or_key}/sla"
    primary_keys = ("issueId", "id",)
    records_jsonpath = "$.values[*]"
    parent_stream_type = RequestStream

    schema = PropertiesList(
        Property("issueId", StringType),
        Property("issueKey", StringType),
        Property("id", StringType, required=True),
        Property("name", StringType),
        Property("ongoingCycle", SlaCycleType),
        Property("completedCycles", ArrayType(SlaCycleType)),
    ).to_dict()

    @override
    def post_process(
        self,
        row: Record,
        context: Context | None = None,
    ) -> Record | None:
        """Post-process the record before it is returned."""
        if context:
            row["issueKey"] = context.get("issue_key")
            row["issueId"] = context.get("issue_id")
        return row


class RequestStatusStream(JiraServiceManagementPaginatedStream):
    """Stream for status history of a request.

    This stream extracts the history of status changes for a request,
    showing how the request has progressed through different statuses
    over time.

    Parent: RequestStream (provides issue_id_or_key context)

    API Reference:
        https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-request/#api-rest-servicedeskapi-request-issueidorkey-status-get
    """

    name = "request_status"
    path = "/request/{issue_id_or_key}/status"
    primary_keys = ("issueId", "status", "statusDate",)
    records_jsonpath = "$.values[*]"
    parent_stream_type = RequestStream

    schema = PropertiesList(
        Property("issueId", StringType),
        Property("issueKey", StringType),
        Property("status", StringType, required=True),
        Property("statusCategory", StringType),
        Property("statusDate", JsmDateType, required=True),
    ).to_dict()

    @override
    def post_process(
        self,
        row: Record,
        context: Context | None = None,
    ) -> Record | None:
        """Post-process the record before it is returned."""
        if context:
            row["issueKey"] = context.get("issue_key")
            row["issueId"] = context.get("issue_id")
        return row
