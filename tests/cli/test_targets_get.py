import json
import re
from unittest.mock import patch, Mock, call

import pytest

from probely_cli.cli.common import RiskEnum


@patch("probely_cli.cli.commands.targets.get.list_targets")
def test_targets_get__table_headers_output(
    sdk_list_targets_mock: Mock,
    valid_get_targets_api_response: dict,
    probely_cli,
) -> None:
    sdk_list_targets_mock.return_value = valid_get_targets_api_response["results"]

    stdout, stderr = probely_cli("targets", "get", return_list=True)

    table_header = stdout[0]
    assert "ID" in table_header
    assert "NAME" in table_header
    assert "URL" in table_header
    assert "RISK" in table_header
    assert "LAST_SCAN" in table_header
    assert "LABELS" in table_header

    assert len(stderr) == 0


@pytest.mark.parametrize(
    "testing_value,expected_output",
    [
        (None, "Never scanned"),
        ({}, "Never scanned"),
        ({"started": None}, "Never scanned"),
        ({"started": "2024-07-15T15:47:52.608557Z"}, "2024-07-15 15:07"),
    ],
)
@patch("probely_cli.cli.commands.targets.get.list_targets")
def test_targets_get__table_last_scan_date_output(
    sdk_list_targets_mock: Mock,
    testing_value,
    expected_output,
    probely_cli,
    valid_get_targets_api_response,
):
    testable_target_result = valid_get_targets_api_response["results"][0]
    testable_target_result["last_scan"] = testing_value

    sdk_list_targets_mock.return_value = [testable_target_result]

    stdout, stderr = probely_cli("targets", "get", return_list=True)

    assert len(stderr) == 0

    column_separator = "  "  # double space

    table_header = stdout[0]
    table_columns = table_header.split()
    assert table_columns[4] == "LAST_SCAN"

    target_line = stdout[1].strip()
    target_line = re.sub(r" {3,}", "  ", target_line)
    target_columns = target_line.split(column_separator)
    assert target_columns[4] == expected_output


@pytest.mark.parametrize(
    "testing_value,expected_output",
    [
        (0, RiskEnum.NO_RISK.name),
        (10, RiskEnum.LOW.name),
        (20, RiskEnum.NORMAL.name),
        (30, RiskEnum.HIGH.name),
        (None, RiskEnum.NA.name),
        (323232320, "Unknown"),
        ("323232320", "Unknown"),
    ],
)
@patch("probely_cli.cli.commands.targets.get.list_targets")
def test_targets_get__table_risk_output(
    sdk_list_targets_mock: Mock,
    testing_value,
    expected_output,
    valid_get_targets_api_response,
    probely_cli,
):
    testable_target_result = valid_get_targets_api_response["results"][0]
    testable_target_result["risk"] = testing_value
    sdk_list_targets_mock.return_value = [testable_target_result]

    stdout, stderr = probely_cli("targets", "get", return_list=True)

    assert len(stderr) == 0
    column_separator = "  "  # double space

    table_header = stdout[0]
    table_columns = table_header.split()
    assert table_columns[3] == "RISK"

    target_line = stdout[1]
    target_line = re.sub(r" {3,}", "  ", target_line)
    target_line = target_line.strip()
    target_columns = target_line.split(column_separator)
    assert target_columns[3] == expected_output


@pytest.mark.parametrize(
    "testing_value,expected_output",
    [
        ([{"name": "one"}], "one"),
        ([{"name": "one"}, {"name": "two"}], "one, two"),
        (None, "Unknown labels"),
        ([{"no_name_key": "no"}], "Unknown labels"),
    ],
)
@patch("probely_cli.cli.commands.targets.get.list_targets")
def test_targets_get__table_labels_output(
    sdk_list_targets_mock: Mock,
    testing_value,
    expected_output,
    valid_get_targets_api_response,
    probely_cli,
):
    testable_target_result = valid_get_targets_api_response["results"][0]
    testable_target_result["labels"] = testing_value
    sdk_list_targets_mock.return_value = [testable_target_result]

    stdout, stderr = probely_cli("targets", "get", return_list=True)

    assert len(stderr) == 0
    column_separator = "  "  # double space

    table_header = stdout[0]
    table_columns = table_header.split()
    assert table_columns[5] == "LABELS"

    target_line = stdout[1].strip()
    target_line = re.sub(r" {3,}", "  ", target_line)
    target_columns = target_line.split(column_separator)
    assert target_columns[5] == expected_output


@pytest.mark.parametrize(
    "filter_arg, expected_filter_request",
    [
        ("--f-has-unlimited-scans=True", {"unlimited": True}),
        ("--f-has-unlimited-scans=False", {"unlimited": False}),
        ("--f-is-url-verified=1", {"verified": True}),
        ("--f-is-url-verified=0", {"verified": False}),
    ],
)
@patch("probely_cli.cli.commands.targets.get.list_targets")
def test_targets_get__arg_filters_success(
    sdk_list_targets_mock: Mock,
    filter_arg,
    expected_filter_request,
    probely_cli,
):
    probely_cli("targets", "get", filter_arg)

    expected_call_args = call(target_filters=expected_filter_request)
    assert sdk_list_targets_mock.call_args == expected_call_args


@pytest.mark.parametrize(
    "filter_arg, expected_error_message",
    [
        (
            "--f-has-unlimited-scans=None",
            "{'f_has_unlimited_scans': ['Not a valid boolean.']}",
        ),
        (
            "--f-has-unlimited-scans=meh",
            "{'f_has_unlimited_scans': ['Not a valid boolean.']}",
        ),
        (
            "--f-has-unlimited-scans=",
            "{'f_has_unlimited_scans': ['Not a valid boolean.']}",
        ),
        (
            "--f-is-url-verified=None",
            "{'f_is_url_verified': ['Not a valid boolean.']}",
        ),
        (
            "--f-is-url-verified=meh",
            "{'f_is_url_verified': ['Not a valid boolean.']}",
        ),
        (
            "--f-is-url-verified=",
            "{'f_is_url_verified': ['Not a valid boolean.']}",
        ),
    ],
)
@patch("probely_cli.cli.commands.targets.get.list_targets")
def test_targets_get__arg_filters_validations(
    # sdk_list_targets_mock: Mock,
    _: Mock,
    filter_arg,
    expected_error_message,
    probely_cli,
):
    _, stderr_lines = probely_cli("targets", "get", filter_arg, return_list=True)

    assert len(stderr_lines) == 1

    error_message = stderr_lines[0]
    assert error_message == expected_error_message
