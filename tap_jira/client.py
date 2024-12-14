"""REST client handling, including tap-jiraStream base class."""

from __future__ import annotations

import typing as t
from pathlib import Path

import requests
import requests.auth
from singer_sdk.streams import RESTStream

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context

_Auth = t.Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class JiraStream(RESTStream):
    """tap-jira stream class."""

    next_page_token_jsonpath = "$.paging.start"  # noqa: S105
    records_jsonpath = "$[*]"  # Or override `parse_response`.
    instance_name: str

    @property
    def url_base(self) -> str:
        """Returns base url."""
        domain = self.config["domain"]
        return f"https://{domain}:443/rest/api/3"

    @property
    def authenticator(self) -> _Auth:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return requests.auth.HTTPBasicAuth(
            password=self.config["api_token"],
            username=self.config["email"],
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")  # noqa: ERA001
        return headers

    def get_url_params(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
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
        previous_token: t.Any | None,  # noqa: ANN401
    ) -> t.Any | None:  # noqa: ANN401
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
