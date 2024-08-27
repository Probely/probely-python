import re
from unittest.mock import Mock, patch

import pytest

from probely_cli.cli.common import TargetRiskEnum


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
        (0, TargetRiskEnum.NO_RISK.name),
        (10, TargetRiskEnum.LOW.name),
        (20, TargetRiskEnum.NORMAL.name),
        (30, TargetRiskEnum.HIGH.name),
        (None, TargetRiskEnum.NA.name),
        (323232320, "Unknown"),
        ("323232320", "Unknown"),
        ("10", "Unknown"),
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
        (None, "Unknown_labels"),
        ([{"no_name_key": "no"}], "Unknown_labels"),
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
