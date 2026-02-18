"""REST client handling, including tap-jiraStream base class."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, TypeVar

import requests.auth
from singer_sdk.streams import RESTStream

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    from collections.abc import Callable

    from requests import Response
    from singer_sdk.helpers.types import Context

    _Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]


_TNextPageToken = TypeVar("_TNextPageToken")


class JiraStream(RESTStream[_TNextPageToken]):
    """tap-jira stream class."""

    next_page_token_jsonpath = "$.paging.start"  # noqa: S105
    records_jsonpath = "$[*]"  # Or override `parse_response`.
    instance_name: str

    @override
    @property
    def url_base(self) -> str:
        """Returns base url."""
        domain = self.config["domain"]
        return f"https://{domain}:443/rest/api/3"

    @override
    @property
    def authenticator(self) -> _Auth:
        """Stream authenticator."""
        return requests.auth.HTTPBasicAuth(
            password=self.config["api_token"],
            username=self.config["email"],
        )

    @override
    def validate_response(self, response: requests.Response) -> None:
        """Validate HTTP response, allowing 403 to be skipped."""
        if response.status_code == 403:
            self.logger.warning(
                f"Access denied (403) for {response.url}. Skipping."
            )
            return  # Don't raise, just skip this resource
        super().validate_response(response)

class JiraStartAtPaginatedStream(JiraStream[int]):
    """Jira stream that uses the startAt pagination parameter."""

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: int | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict[str, Any] = {}
        if next_page_token:
            params["startAt"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def get_next_page_token(
        self,
        response: Response,
        previous_token: int | None,
    ) -> int | None:
        """Return a token for identifying next page or None if no more pages."""
        # If pagination is required, return a token which can be used to get the
        #       next page. If this is the final page, return "None" to end the
        #       pagination loop.
        resp_json = response.json()

        if previous_token is None:
            previous_token = 0

        total = -1
        results = 0
        _value = None
        is_last = None

        if (
            isinstance(resp_json, dict)
            and resp_json.get(self.instance_name) is not None
        ):
            _value = resp_json.get(self.instance_name)
            total = resp_json.get("total", -1)
            is_last = resp_json.get("isLast")
            results = len(_value)  # type: ignore[arg-type]

        if isinstance(is_last, bool) and total == -1 and not is_last:
            return previous_token + results

        if _value is None:
            page = resp_json
            if len(page) == 0 or total <= previous_token + results:
                return None
        elif len(_value) == 0 or total <= previous_token + results:
            return None

        return previous_token + results

class JiraServiceManagementStream(RESTStream[_TNextPageToken]):
    """Base stream class for Jira Service Management (JSM) API endpoints.

    This class provides the foundation for all streams that interact with the
    Jira Service Management REST API (servicedeskapi), which is separate from
    the standard Jira REST API (api/3).

    Key differences from JiraStream:
        - Uses `/rest/servicedeskapi` as the base URL instead of `/rest/api/3`
        - Handles 403 responses gracefully by logging a warning and skipping
          the resource, rather than raising an exception

    Attributes:
        next_page_token_jsonpath: JSONPath to extract pagination token from response.
        records_jsonpath: JSONPath to extract records from response.
    """

    next_page_token_jsonpath = "$.paging.start"  # noqa: S105
    records_jsonpath = "$[*]"  # Or override `parse_response`.

    @override
    @property
    def url_base(self) -> str:
        """Returns base url."""
        domain = self.config["domain"]
        return f"https://{domain}:443/rest/servicedeskapi"

    @override
    @property
    def authenticator(self) -> _Auth:
        """Stream authenticator."""
        return requests.auth.HTTPBasicAuth(
            password=self.config["api_token"],
            username=self.config["email"],
        )

    @override
    def validate_response(self, response: requests.Response) -> None:
        """Validate HTTP response, allowing 403 to be skipped."""
        if response.status_code == 403:
            self.logger.warning(
                f"Access denied (403) for {response.url}. Skipping."
            )
            return  # Don't raise, just skip this resource
        super().validate_response(response)

class JiraServiceManagementPaginatedStream(JiraServiceManagementStream[int]):
    """Paginated stream class for Jira Service Management API endpoints.

    Extends JiraServiceManagementStream with pagination support using the
    `start` parameter. The JSM API uses offset-based pagination where:
        - `start`: The starting index of the returned objects (0-based)
        - `size`: The number of items returned per page
        - `isLastPage`: Boolean indicating if this is the final page

    Pagination continues until `isLastPage` is True, incrementing the start
    offset by the page size for each subsequent request.
    """

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: int | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict[str, Any] = {}
        if next_page_token:
            params["start"] = next_page_token

        return params

    def get_next_page_token(
        self,
        response: Response,
        previous_token: int | None,
    ) -> int | None:
        """Return a token for identifying next page or None if no more pages."""
        # If pagination is required, return a token which can be used to get the
        #       next page. If this is the final page, return "None" to end the
        #       pagination loop.
        resp_json = response.json()

        if previous_token is None:
            previous_token = 0

        start = resp_json.get("start")
        size = resp_json.get("size")
        is_last = resp_json.get("isLastPage")

        if is_last != True and isinstance(start, int) and isinstance(size, int):
            return start + size

        return None
