import re
from unittest.mock import Mock, patch

import pytest

from probely_cli.cli.common import FindingSeverityEnum, FindingStateEnum
from tests.testable_api_responses import RETRIEVE_FINDING_200_RESPONSE


@patch("probely_cli.cli.commands.findings.get.list_findings")
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
@patch("probely_cli.cli.commands.findings.get.list_findings")
def test_findings_get__table_last_found_date_output(
    sdk_list_findings_mock: Mock,
    testing_value,
    expected_output,
    valid_get_findings_api_response,
    probely_cli,
):
    testable_finding = valid_get_findings_api_response["results"][0]
    testable_finding["last_found"] = testing_value

    sdk_list_findings_mock.return_value = [testable_finding]

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
        (0, "UNKNOWN"),
        (10, FindingSeverityEnum.LOW.name),
        (20, FindingSeverityEnum.NORMAL.name),
        (30, FindingSeverityEnum.HIGH.name),
        (None, "UNKNOWN"),
        (323232320, "UNKNOWN"),
        ("323232320", "UNKNOWN"),
        ("10", "UNKNOWN"),
    ],
)
@patch("probely_cli.cli.commands.findings.get.list_findings")
def test_findings_get__table_severity_output(
    sdk_list_findings_mock: Mock,
    testing_value,
    expected_output,
    valid_get_findings_api_response,
    probely_cli,
):
    testable_finding = valid_get_findings_api_response["results"][0]
    testable_finding["severity"] = testing_value
    sdk_list_findings_mock.return_value = [testable_finding]

    stdout, stderr = probely_cli("findings", "get", return_list=True)

    assert len(stderr) == 0
    column_separator = "  "  # double space

    table_header = stdout[0]
    table_columns = table_header.split()
    assert table_columns[2] == "SEVERITY"

    finding_line = stdout[1]
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
        (None, "UNKNOWN_LABELS"),
        ([{"no_name_key": "no"}], "UNKNOWN_LABELS"),
    ],
)
@patch("probely_cli.cli.commands.findings.get.list_findings")
def test_findings_get__table_labels_output(
    sdk_list_findings_mock: Mock,
    testing_value,
    expected_output,
    valid_get_findings_api_response,
    probely_cli,
):
    testable_finding = valid_get_findings_api_response["results"][0]
    testable_finding["labels"] = testing_value
    sdk_list_findings_mock.return_value = [testable_finding]

    stdout, stderr = probely_cli("findings", "get", return_list=True)

    assert len(stderr) == 0
    column_separator = "  "  # double space

    table_header = stdout[0]
    table_columns = table_header.split()

    assert table_columns[6] == "LABELS"

    finding_line = stdout[1].strip()
    three_spaces_pattern = r" {3,}"
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
            f"--f-severity={FindingSeverityEnum.NORMAL.name}",
            {"severity": [FindingSeverityEnum.NORMAL.api_filter_value]},
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
@patch("probely_cli.cli.commands.findings.get.list_findings")
def test_findings_get__arg_filters_success(
    sdk_list_findings_mock: Mock,
    filter_arg,
    expected_filter_request,
    probely_cli,
):
    stdout, stderr = probely_cli("findings", "get", filter_arg, return_list=True)

    assert len(stderr) == 0, "Expected no errors"
    sdk_list_findings_mock.assert_called_once_with(
        findings_filters=expected_filter_request
    )


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
            "error: argument --f-severity: invalid choice: 'INVALID_VALUE' (choose from 'LOW', 'NORMAL', 'HIGH')",
        ),
        (
            "--f-severity invalid_value",
            "error: argument --f-severity: invalid choice: 'INVALID_VALUE' (choose from 'LOW', 'NORMAL', 'HIGH')",
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
@patch("probely_cli.cli.commands.findings.get.list_findings")
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


@patch("probely_cli.cli.commands.findings.get.retrieve_findings")
def test_findings_get__retrieve_by_ids(retrieve_findings_mock: Mock, probely_cli):
    finding_id1 = "finding_id1"
    finding_id2 = "finding_id2"

    finding_id1_content = RETRIEVE_FINDING_200_RESPONSE.copy()
    finding_id2_content = RETRIEVE_FINDING_200_RESPONSE.copy()

    finding_id1_content["id"] = finding_id1
    finding_id2_content["id"] = finding_id2

    retrieve_findings_mock.return_value = [finding_id1_content, finding_id2_content]

    stdout_lines, stderr_lines = probely_cli(
        "findings",
        "get",
        finding_id1,
        finding_id2,
        return_list=True,
    )

    retrieve_findings_mock.assert_called_once_with(
        findings_ids=[finding_id1, finding_id2]
    )
    assert len(stderr_lines) == 0
    assert (
        len(stdout_lines) == 3
    ), "Expected to have header and 2 entries for each target"
    assert finding_id1 in stdout_lines[1]
    assert finding_id2 in stdout_lines[2]


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
        "probely findings get: error: filters and finding ids are mutually exclusive."
    )
