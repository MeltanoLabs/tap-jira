# tap-jira
 
# tap-jira
 
`tap-jira` is a Singer tap for tap-jira.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`
* `schema-flattening`

## Configuration

### Accepted Config Options

| Setting             | Required | Default | Description |
|:--------------------|:--------:|:-------:|:------------|
| username            | True    | None    | The username to authenticate against the API service |
| password            | True    | None    | The password to authenticate against the API service |
| api_version_2       | True    | v2.0    | The API version to request data from. |
| api_version_3       | True    | v3.0    | The API version to request data from. |
| agile_version       | True    | v1.0    | The Agile version to request data from. |
| board_id            | True    | 63      | The Jira board id to request data from. |
| account_id          | True    | None    | The Jira account id. |
| project_id          | True    | None    | The Jira project id. |
| role_admin_id       | True    | None    | The Jira role admin id. |
| role_viewer_id      | True    | None    | The Jira role viewer id. |
| role_member_id      | True    | None    | The Jira role member id. |
| role_altasian_id    | True    | None    | The Jira role altasian id. |
| auth_type           | True    | basic   | The auth type to select authentication (basic/http). |
| start_date          | False   | None    | The earliest record date to sync |
| end_date            | False   | None    | The latest record date to sync |
| stream_maps         | False   | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config   | False   | None    | User-defined config values to be used within map expressions. |
| flattening_enabled  | False   | None    | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth| False   | None    | The max depth to flatten schemas. |

### Meltano Variables

The following config values need to be set in order to use with Meltano. These can be set in `meltano.yml`, via
```meltano config tap-jira set --interactive```, or via the env var mappings shown above.

- `username:` username from TAP_JIRA_USERNAME variable
- `password:` password from TAP_JIRA_PASSWORD variable
- `start_date:` start date
- `end_date:` end_date
- `api_version_2:` api version
- `api_version_3:` api version
- `agile_version:` agile version
- `board_id:` board id
- `account_id:` account id
- `project_id:` project id
- `role_admin_id:` role admin id
- `role_viewer_id:` role viewer id
- `role_member_id:` role member id
- `role_altasian_id:` role altasian id
- `auth_type:` auth type

A full list of supported settings and capabilities for this tap is available by running:

```bash
tap-jira --about
```

## Elastic License 2.0

The licensor grants you a non-exclusive, royalty-free, worldwide, non-sublicensable, non-transferable license to use, copy, distribute, make available, and prepare derivative works of the software.

## Installation

```bash
pipx install git+https://github.com/ryan-miranda-partners/tap-jira.git
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

A Jira username and password are required to make API requests. (See [Jira API](https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/) docs for more info)

## Usage

You can easily run `tap-jira` by itself or in a pipeline using [Meltano](https://meltano.com/).

## Stream Inheritance

This project uses parent-child streams. Learn more about them [here](https://gitlab.com/meltano/sdk/-/blob/main/docs/parent_streams.md).

### Executing the Tap Directly

```bash
tap-jira --version
tap-jira --help
tap-jira --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-jira` CLI interface directly using `poetry run`:

```bash
poetry run tap-jira --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any "TODO" items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-jira
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-jira --version
# OR run a test `elt` pipeline:
meltano elt tap-jira target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
