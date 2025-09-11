# tap-jira

tap-jira tap class.

Built with the [Meltano Singer SDK](https://sdk.meltano.com).

## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`
* `schema-flattening`
* `batch`

## Supported Python Versions

* 3.10
* 3.11
* 3.12
* 3.13

## Settings

| Setting                      | Required | Default    | Description                                                                      |
|:-----------------------------|:---------|:-----------|:---------------------------------------------------------------------------------|
| start_date                   | False    | None       | Earliest record date to sync                                                     |
| end_date                     | False    | None       | Latest record date to sync                                                       |
| domain                       | True     | None       | The Domain for your Jira account, e.g. meltano.atlassian.net                     |
| api_token                    | True     | None       | Jira API Token.                                                                  |
| email                        | True     | None       | The user email for your Jira account.                                            |
| page_size                    | False    | None       |                                                                                  |
| page_size.issues             | False    | 100        | Page size for issues stream                                                      |
| stream_options               | False    | None       | Options for individual streams                                                   |
| stream_options.issues        | False    | None       | Options specific to the issues stream                                            |
| stream_options.issues.jql    | False    | id != null | A JQL query to filter issues                                                     |
| stream_options.issues.fields | False    | *all       | A comma-separated list of fields to include. All fields are included by default. |
| include_audit_logs           | False    | False      | Include the audit logs stream                                                    |

### Built-in capabilities

| Setting                           | Required | Default | Description                                                                                                                                                                                                                                              |
| :-------------------------------- | :------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| stream_maps                       | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html).                                                                                                              |
| stream_map_config                 | False    | None    | User-defined config values to be used within map expressions.                                                                                                                                                                                            |
| faker_config                      | False    | None    | Config for the [`Faker`](https://faker.readthedocs.io/en/master/) instance variable `fake` used within map expressions. Only applicable if the plugin specifies `faker` as an addtional dependency (through the `singer-sdk` `faker` extra or directly). |
| faker_config.seed                 | False    | None    | Value to seed the Faker generator for deterministic output: https://faker.readthedocs.io/en/master/#seeding-the-generator                                                                                                                                |
| faker_config.locale               | False    | None    | One or more LCID locale strings to produce localized output for: https://faker.readthedocs.io/en/master/#localization                                                                                                                                    |
| flattening_enabled                | False    | None    | 'True' to enable schema flattening and automatically expand nested properties.                                                                                                                                                                           |
| flattening_max_depth              | False    | None    | The max depth to flatten schemas.                                                                                                                                                                                                                        |
| batch_config                      | False    | None    | Configuration for BATCH message capabilities.                                                                                                                                                                                                            |
| batch_config.encoding             | False    | None    | Specifies the format and compression of the batch files.                                                                                                                                                                                                 |
| batch_config.encoding.format      | False    | None    | Format to use for batch files.                                                                                                                                                                                                                           |
| batch_config.encoding.compression | False    | None    | Compression format to use for batch files.                                                                                                                                                                                                               |
| batch_config.storage              | False    | None    | Defines the storage layer to use when writing batch files                                                                                                                                                                                                |
| batch_config.storage.root         | False    | None    | Root path to use when writing batch files.                                                                                                                                                                                                               |
| batch_config.storage.prefix       | False    | None    | Prefix to use when writing batch files.                                                                                                                                                                                                                  |

A full list of supported settings and capabilities is available by running: `tap-jira --about`

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
