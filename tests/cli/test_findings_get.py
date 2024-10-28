import json
import re
from unittest.mock import Mock, patch

import pytest
import yaml

from probely.sdk.enums import FindingSeverityEnum, FindingStateEnum
from probely.sdk.models import Finding
from probely.sdk._schemas import Finding as FindingDataModel
from probely.sdk._schemas import FindingLabel
from tests.testable_api_responses import RETRIEVE_FINDING_200_RESPONSE


@pytest.mark.skip(reason="Skipping this test temporarily")
@patch("probely.cli.commands.findings.get.list_findings")
def test_findings_get__table_headers_output(
    sdk_list_findings_mock: Mock,
    probely_cli,
):
    sdk_list_findings_mock.return_value = []

    stdout, stderr = probely_cli("findings", "get", return_list=True)

    assert len(stderr) == 0

    assert len(stdout) == 1, "Expected header, even on empty list"

    table_header = stdout[0]
    assert "ID" in table_header
    assert "TARGET_ID" in table_header
    assert "SEVERITY" in table_header
    assert "TITLE" in table_header
    assert "LAST_FOUND" in table_header
    assert "STATE" in table_header
    assert "LABELS" in table_header


@pytest.mark.parametrize(
    "testing_value,expected_output",
    [
        # (None, "NO_DATE"),
        ("2024-07-15T17:27:52.608557Z", "2024-07-15 17:27"),
    ],
)
@patch("probely.cli.commands.findings.get.FindingManager.list")
def test_findings_get__table_last_found_date_output(
    sdk_list_findings_mock: Mock,
    testing_value,
    expected_output,
    valid_get_findings_api_response,
    probely_cli,
):
    testable_finding = valid_get_findings_api_response["results"][0]
    testable_finding["last_found"] = testing_value

    sdk_list_findings_mock.return_value = [
        Finding(FindingDataModel(**testable_finding))
    ]

    stdout, stderr = probely_cli("findings", "get", return_list=True)

    assert len(stderr) == 0

    column_separator = "  "  # double space

    table_header = stdout[0]
    table_columns = table_header.split()
    assert table_columns[4] == "LAST_FOUND"

    finding_line = stdout[1].strip()
    finding_line_without_extra_spaces = re.sub(r" {3,}", "  ", finding_line)
    finding_columns = finding_line_without_extra_spaces.split(column_separator)
    assert finding_columns[4] == expected_output


@pytest.mark.parametrize(
    "testing_value,expected_output",
    [
        (10, FindingSeverityEnum.LOW.name),
        (20, FindingSeverityEnum.MEDIUM.name),
        (30, FindingSeverityEnum.HIGH.name),
    ],
)
@patch("probely.cli.commands.findings.get.FindingManager.list")
def test_findings_get__table_severity_output(
    sdk_list_findings_mock: Mock,
    testing_value,
    expected_output,
    valid_get_findings_api_response,
    probely_cli,
):
    testable_finding = valid_get_findings_api_response["results"][0]
    testable_finding["severity"] = testing_value
    sdk_list_findings_mock.return_value = [
        Finding(FindingDataModel(**testable_finding))
    ]

    stdout_lines, stderr_lines = probely_cli("findings", "get", return_list=True)

    assert len(stderr_lines) == 0
    column_separator = "  "  # double space

    table_header = stdout_lines[0]
    table_columns = table_header.split()
    assert table_columns[2] == "SEVERITY"

    finding_line = stdout_lines[1]
    three_spaces_pattern = r" {3,}"
    finding_line_without_extra_spaces = re.sub(
        three_spaces_pattern,
        column_separator,
        finding_line,
    )
    finding_line_without_extra_spaces = finding_line_without_extra_spaces.strip()
    finding_columns = finding_line_without_extra_spaces.split(column_separator)
    assert finding_columns[2] == expected_output


@pytest.mark.parametrize(
    "testing_value,expected_output",
    [
        ([{"name": "one"}], "one"),
        ([{"name": "one"}, {"name": "two"}], "one, two"),
        ([], ""),
    ],
)
@patch("probely.cli.commands.findings.get.FindingManager.list")
def test_findings_get__table_labels_output(
    sdk_list_findings_mock: Mock,
    testing_value,
    expected_output,
    valid_get_findings_api_response,
    probely_cli,
):
    testable_finding_response_data = valid_get_findings_api_response["results"][0]
    finding = Finding(FindingDataModel(**testable_finding_response_data))

    if testing_value:
        finding._data.labels = [
            FindingLabel.model_construct(**label_data) for label_data in testing_value
        ]
    else:
        finding._data.labels = testing_value

    sdk_list_findings_mock.return_value = [finding]

    stdout_lines, stderr_lines = probely_cli("findings", "get", return_list=True)

    assert len(stderr_lines) == 0

    table_header = stdout_lines[0]
    table_columns = table_header.split()

    assert table_columns[6] == "LABELS"

    finding_line = stdout_lines[1]
    three_spaces_pattern = r" {3,}"
    column_separator = "  "  # double space
    finding_line_without_extra_spaces = re.sub(
        three_spaces_pattern,
        column_separator,
        finding_line,
    )

    finding_columns = finding_line_without_extra_spaces.split(column_separator)
    assert finding_columns[6] == expected_output


@pytest.mark.parametrize(
    "filter_arg, expected_filter_request",
    [
        ("--f-scans id1", {"scan": ["id1"]}),
        ("--f-scans=id1", {"scan": ["id1"]}),
        ("--f-scans id1 id2", {"scan": ["id1", "id2"]}),
        (
            f"--f-severity {FindingSeverityEnum.LOW.name}",
            {"severity": [FindingSeverityEnum.LOW.api_filter_value]},
        ),
        (
            f"--f-severity={FindingSeverityEnum.MEDIUM.name}",
            {"severity": [FindingSeverityEnum.MEDIUM.api_filter_value]},
        ),
        (
            f"--f-severity {FindingSeverityEnum.LOW.name} {FindingSeverityEnum.HIGH.name}",
            {
                "severity": [
                    FindingSeverityEnum.LOW.api_filter_value,
                    FindingSeverityEnum.HIGH.api_filter_value,
                ]
            },
        ),
        (
            f"--f-severity {FindingSeverityEnum.LOW.name.lower()}",
            {"severity": [FindingSeverityEnum.LOW.api_filter_value]},
        ),
        (
            f"--f-state {FindingStateEnum.FIXED.name}",
            {"state": [FindingStateEnum.FIXED.api_filter_value]},
        ),
        (
            f"--f-state={FindingStateEnum.NOT_FIXED.name}",
            {"state": [FindingStateEnum.NOT_FIXED.api_filter_value]},
        ),
        (
            f"--f-state {FindingStateEnum.ACCEPTED.name} {FindingStateEnum.FIXED.name}",
            {
                "state": [
                    FindingStateEnum.ACCEPTED.api_filter_value,
                    FindingStateEnum.FIXED.api_filter_value,
                ]
            },
        ),
        (
            f"--f-state {FindingStateEnum.FIXED.name.lower()}",
            {"state": [FindingStateEnum.FIXED.api_filter_value]},
        ),
        (
            "--f-targets xxx ",
            {"target": ["xxx"]},
        ),
        (
            "--f-targets id1 id2",
            {"target": ["id1", "id2"]},
        ),
        ("--f-search hello", {"search": "hello"}),
        ("--f-is-new true", {"new": True}),
        ("--f-is-new false", {"new": False}),
    ],
)
@patch("probely.cli.commands.findings.get.FindingManager.list")
def test_findings_get__arg_filters_success(
    sdk_list_findings_mock: Mock,
    filter_arg,
    expected_filter_request,
    probely_cli,
):
    stdout_lines, stderr_lines = probely_cli(
        "findings", "get", filter_arg, return_list=True
    )

    assert len(stderr_lines) == 0, "Expected no errors"
    sdk_list_findings_mock.assert_called_once_with(filters=expected_filter_request)


@pytest.mark.parametrize(
    "filter_arg, expected_error_content",
    [
        (
            "--f-scans",
            "error: argument --f-scans: expected at least one argument",
        ),
        (
            "--f-severity",
            "error: argument --f-severity: expected at least one argument",
        ),
        (
            "--f-severity=invalid_value",
            "error: argument --f-severity: invalid choice: 'INVALID_VALUE' (choose from 'LOW', 'MEDIUM', 'HIGH')",
        ),
        (
            "--f-severity invalid_value",
            "error: argument --f-severity: invalid choice: 'INVALID_VALUE' (choose from 'LOW', 'MEDIUM', 'HIGH')",
        ),
        (
            "--f-state",
            "error: argument --f-state: expected at least one argument",
        ),
        (
            "--f-state=invalid_value",
            "error: argument --f-state: invalid choice: 'INVALID_VALUE' (choose from 'FIXED', 'NOT_FIXED', 'ACCEPTED', 'RETESTING')",
        ),
        (
            "--f-state invalid_value",
            "error: argument --f-state: invalid choice: 'INVALID_VALUE' (choose from 'FIXED', 'NOT_FIXED', 'ACCEPTED', 'RETESTING')",
        ),
        (
            "--f-targets",
            "error: argument --f-targets: expected at least one argument",
        ),
        (
            "--f-search",
            "error: argument --f-search: expected one argument",
        ),
        (
            "--f-is-new",
            "error: argument --f-is-new: expected one argument",
        ),
        (
            "--f-is-new xxx",
            "error: argument --f-is-new: invalid choice: 'XXX' (choose from 'TRUE', 'FALSE')",
        ),
    ],
)
@patch("probely.cli.commands.findings.get.FindingManager.list")
def test_findings_get__arg_filters_validations(
    _: Mock,
    filter_arg,
    expected_error_content,
    probely_cli,
):
    stdout_lines, stderr_lines = probely_cli(
        "findings", "get", filter_arg, return_list=True
    )

    assert len(stdout_lines) == 0, "Expected no output"
    assert len(stderr_lines) >= 1, "Expected error output"

    error_message = stderr_lines[-1]
    assert expected_error_content in error_message


@patch("probely.cli.commands.findings.get.FindingManager.get_multiple")
def test_findings_get__retrieve_by_ids(get_multiple_findings_mock: Mock, probely_cli):
    finding1_id = "1111"
    finding2_id = "2222"

    finding1_response_data = RETRIEVE_FINDING_200_RESPONSE.copy()
    finding2_response_data = RETRIEVE_FINDING_200_RESPONSE.copy()

    finding1_response_data["id"] = finding1_id
    finding2_response_data["id"] = finding2_id

    get_multiple_findings_mock.return_value = [
        Finding(FindingDataModel(**finding1_response_data)),
        Finding(FindingDataModel(**finding2_response_data)),
    ]

    stdout_lines, stderr_lines = probely_cli(
        "findings",
        "get",
        finding1_id,
        finding2_id,
        return_list=True,
    )

    get_multiple_findings_mock.assert_called_once_with(ids=[finding1_id, finding2_id])
    assert len(stderr_lines) == 0
    assert (
        len(stdout_lines) == 3
    ), "Expected to have header and 2 entries for each target"
    assert finding1_id in stdout_lines[1]
    assert finding2_id in stdout_lines[2]


def test_findings_get__mutually_exclusive_arguments(probely_cli):
    stdout_lines, stderr_lines = probely_cli(
        "findings",
        "get",
        "id1 id2",
        "--f-severity low",
        return_list=True,
    )

    assert len(stdout_lines) == 0, "Expected no output"
    assert len(stderr_lines) == 1, "Expected error output"

    assert stderr_lines[0] == (
        "probely findings get: error: filters and Finding IDs are mutually exclusive."
    )


@patch("probely.cli.commands.findings.get.FindingManager.get_multiple")
def test_targets_get__output_argument_output(get_multiple_findings_mock, probely_cli):
    finding1_id = "1111"
    finding2_id = "2222"

    finding1_response_data = RETRIEVE_FINDING_200_RESPONSE.copy()
    finding2_response_data = RETRIEVE_FINDING_200_RESPONSE.copy()

    finding1_response_data["id"] = finding1_id
    finding2_response_data["id"] = finding2_id

    get_multiple_findings_mock.return_value = [
        Finding(FindingDataModel(**finding1_response_data)),
        Finding(FindingDataModel(**finding2_response_data)),
    ]

    stdout, _ = probely_cli(
        "findings",
        "get",
        str(finding1_id),
        str(finding2_id),
    )
    header = ("ID", "TARGET_ID", "SEVERITY", "TITLE", "LAST_FOUND", "STATE", "LABELS")
    assert all(column in stdout for column in header), "Output with table expected"
    assert (
        finding1_id in stdout
    ), f"Expected finding1_id {finding1_id} in stdout: {stdout}"
    assert (
        finding2_id in stdout
    ), f"Expected finding1_id {finding2_id} in stdout: {stdout}"

    stdout, stderr = probely_cli("findings", "get", finding1_id, finding2_id, "-o yaml")

    assert stderr == ""
    yaml_content = yaml.load(stdout, Loader=yaml.FullLoader)
    assert isinstance(yaml_content, list), "Expected a yaml list"
    assert len(yaml_content) == 2, "Expected 2 targets"
    assert (
        str(yaml_content[0]["id"]) == finding1_id
    ), "Expected findings_id0  in yaml content"
    assert (
        str(yaml_content[1]["id"]) == finding2_id
    ), "Expected findings_id1 in yaml content"

    stdout, stderr = probely_cli(
        "findings", "get", finding1_id, finding2_id, "--output json"
    )

    assert stderr == ""
    json_content = json.loads(stdout)
    assert isinstance(json_content, list), "Expected a json list"
    assert len(json_content) == 2, "Expected 2 targets"
    assert str(json_content[0]["id"]) == finding1_id, "Expected findings_id0  in json"
    assert str(json_content[1]["id"]) == finding2_id, "Expected findings_id1 in json"
