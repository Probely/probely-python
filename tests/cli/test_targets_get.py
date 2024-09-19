import json
import re
from unittest.mock import patch, Mock

import pytest
import yaml

from probely_cli.cli.common import TargetRiskEnum, TargetTypeEnum
from tests.testable_api_responses import RETRIEVE_TARGET_200_RESPONSE


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
        (None, "Never_scanned"),
        ({}, "Never_scanned"),
        ({"started": None}, "Never_scanned"),
        ({"started": "2024-07-15T15:47:52.608557Z"}, "2024-07-15 15:47"),
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
        (0, TargetRiskEnum.NO_RISK.name),
        (10, TargetRiskEnum.LOW.name),
        (20, TargetRiskEnum.NORMAL.name),
        (30, TargetRiskEnum.HIGH.name),
        (None, TargetRiskEnum.NA.name),
        (323232320, "UNKNOWN"),
        ("323232320", "UNKNOWN"),
        ("10", "UNKNOWN"),
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
    target_line_without_extra_spaces = re.sub(r" {3,}", "  ", target_line)
    target_line_without_extra_spaces = target_line_without_extra_spaces.strip()
    target_columns = target_line_without_extra_spaces.split(column_separator)
    assert target_columns[3] == expected_output


@pytest.mark.parametrize(
    "testing_value,expected_output",
    [
        ([{"name": "one"}], "one"),
        ([{"name": "one"}, {"name": "two"}], "one, two"),
        (None, "UNKNOWN_LABELS"),
        ([{"no_name_key": "no"}], "UNKNOWN_LABELS"),
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
        ("--f-is-url-verified=TRUE", {"verified": True}),
        ("--f-is-url-verified=FALSE", {"verified": False}),
        ("--f-risk=NA", {"risk": ["null"]}),
        ("--f-risk=no_risk", {"risk": [TargetRiskEnum.NO_RISK.api_filter_value]}),
        (
            "--f-risk NA LOW",
            {
                "risk": [
                    TargetRiskEnum.NA.api_filter_value,
                    TargetRiskEnum.LOW.api_filter_value,
                ]
            },
        ),
        (
            "--f-risk high normal",
            {
                "risk": [
                    TargetRiskEnum.HIGH.api_filter_value,
                    TargetRiskEnum.NORMAL.api_filter_value,
                ]
            },
        ),
        (
            "--f-risk NA low",
            {
                "risk": [
                    TargetRiskEnum.NA.api_filter_value,
                    TargetRiskEnum.LOW.api_filter_value,
                ]
            },
        ),
        ("--f-search=meh", {"search": "meh"}),
        ("--f-search=", {"search": ""}),
        ("--f-type=WEB", {"type": [TargetTypeEnum.WEB.api_filter_value]}),
        ("--f-type=API", {"type": [TargetTypeEnum.API.api_filter_value]}),
        ("--f-type=weB", {"type": [TargetTypeEnum.WEB.api_filter_value]}),
        (
            "--f-type weB API",
            {
                "type": [
                    TargetTypeEnum.WEB.api_filter_value,
                    TargetTypeEnum.API.api_filter_value,
                ]
            },
        ),
    ],
)
@patch("probely_cli.cli.commands.targets.get.list_targets")
def test_targets_get__arg_filters_success(
    sdk_list_targets_mock: Mock,
    filter_arg,
    expected_filter_request,
    probely_cli,
):
    stdout, stderr = probely_cli("targets", "get", filter_arg, return_list=True)

    assert len(stderr) == 0, "Expected no errors"
    sdk_list_targets_mock.assert_called_once_with(
        targets_filters=expected_filter_request
    )


@pytest.mark.parametrize(
    "filter_arg, expected_error_content",
    [
        (
            "--f-has-unlimited-scans=None",
            "error: argument --f-has-unlimited-scans: invalid choice: 'NONE' (choose from 'TRUE', 'FALSE')",
        ),
        (
            "--f-has-unlimited-scans=meh",
            "error: argument --f-has-unlimited-scans: invalid choice: 'MEH' (choose from 'TRUE', 'FALSE')",
        ),
        (
            "--f-has-unlimited-scans=",
            "error: argument --f-has-unlimited-scans: invalid choice: '' (choose from 'TRUE', 'FALSE')",
        ),
        (
            "--f-is-url-verified=None",
            "error: argument --f-is-url-verified: invalid choice: 'NONE' (choose from 'TRUE', 'FALSE')",
        ),
        (
            "--f-is-url-verified=meh",
            "error: argument --f-is-url-verified: invalid choice: 'MEH' (choose from 'TRUE', 'FALSE')",
        ),
        (
            "--f-is-url-verified=",
            "error: argument --f-is-url-verified: invalid choice: '' (choose from 'TRUE', 'FALSE')",
        ),
        (
            "--f-risk=random_value",
            "error: argument --f-risk: invalid choice: 'RANDOM_VALUE' (choose from 'NA', 'NO_RISK', 'LOW', 'NORMAL', 'HIGH')",
        ),
        (
            "--f-risk=",
            "error: argument --f-risk: invalid choice: '' (choose from 'NA', 'NO_RISK', 'LOW', 'NORMAL', 'HIGH')",
        ),
        (
            "--f-type=random_value, ",
            "error: argument --f-type: invalid choice: 'RANDOM_VALUE,' (choose from 'WEB', 'API')",
        ),
        (
            "--f-type=",
            "error: argument --f-type: invalid choice: '' (choose from 'WEB', 'API')",
        ),
    ],
)
@patch("probely_cli.cli.commands.targets.get.list_targets")
def test_targets_get__arg_filters_validations(
    _: Mock,
    filter_arg,
    expected_error_content,
    probely_cli,
):
    stdout_lines, stderr_lines = probely_cli(
        "targets", "get", filter_arg, return_list=True
    )

    assert len(stdout_lines) == 0, "Expected no output"
    assert len(stderr_lines) >= 1, "Expected error output"

    error_message = stderr_lines[-1]
    assert expected_error_content in error_message


@patch("probely_cli.cli.commands.targets.get.retrieve_targets")
def test_targets_get__retrieve_by_id(retrieve_targets_mock: Mock, probely_cli):
    target_id1 = "target_id1"
    target_id2 = "target_id2"

    target_id1_content = RETRIEVE_TARGET_200_RESPONSE.copy()
    target_id2_content = RETRIEVE_TARGET_200_RESPONSE.copy()

    target_id1_content["id"] = target_id1
    target_id2_content["id"] = target_id2

    retrieve_targets_mock.return_value = [target_id1_content, target_id2_content]

    stdout_lines, stderr_lines = probely_cli(
        "targets",
        "get",
        target_id1,
        target_id2,
        return_list=True,
    )

    retrieve_targets_mock.assert_called_once_with(targets_ids=[target_id1, target_id2])
    assert len(stderr_lines) == 0
    assert (
        len(stdout_lines) == 3
    ), "Expected to have header and 2 entries for each target"
    assert target_id1 in stdout_lines[1]
    assert target_id2 in stdout_lines[2]


def test_targets_get__mutually_exclusive_arguments(probely_cli):
    stdout_lines, stderr_lines = probely_cli(
        "targets",
        "get",
        "target_id1 target_id2",
        "--f-has-unlimited-scans=True",
        return_list=True,
    )

    assert len(stdout_lines) == 0, "Expected no output"
    assert len(stderr_lines) == 1, "Expected error output"

    assert stderr_lines[0] == (
        "probely targets get: error: filters and Target IDs are mutually exclusive."
    )


@patch("probely_cli.cli.commands.targets.get.retrieve_targets")
def test_targets_get__output_argument_validation(_: Mock, probely_cli):
    stdout_lines, stderr_lines = probely_cli(
        "targets",
        "get",
        "-o",
        "random_text",
        return_list=True,
    )
    assert stdout_lines == []
    assert (
        stderr_lines[-1]
        == "probely targets get: error: argument -o/--output: invalid choice: "
        "'RANDOM_TEXT' (choose from 'YAML', 'JSON')"
    )


@patch("probely_cli.cli.commands.targets.get.retrieve_targets")
def test_targets_get__output_argument_output(retrieve_targets_mock, probely_cli):
    target_id0 = "target_id0"
    target_id1 = "target_id1"

    target_id1_content = RETRIEVE_TARGET_200_RESPONSE.copy()
    target_id2_content = RETRIEVE_TARGET_200_RESPONSE.copy()

    target_id1_content["id"] = target_id0
    target_id2_content["id"] = target_id1

    retrieve_targets_mock.return_value = [target_id1_content, target_id2_content]

    stdout, _ = probely_cli(
        "targets",
        "get",
        target_id0,
        target_id1,
    )
    header = ("ID", "NAME", "URL", "RISK", "LAST_SCAN", "LABELS")
    assert all(column in stdout for column in header), "Output with table expected"
    assert target_id0 in stdout, "target_id0 entry expected"
    assert target_id1 in stdout, "target_id0 entry expected"

    stdout, stderr = probely_cli("targets", "get", target_id0, target_id1, "-o yaml")

    assert stderr == ""
    yaml_content = yaml.load(stdout, Loader=yaml.FullLoader)
    assert isinstance(yaml_content, list), "Expected a yaml list"
    assert len(yaml_content) == 2, "Expected 2 targets"
    assert yaml_content[0]["id"] == target_id0, "Expected target_id0 in yaml content"
    assert yaml_content[1]["id"] == target_id1, "Expected target_id1 in yaml content"

    stdout, stderr = probely_cli(
        "targets", "get", target_id0, target_id1, "--output json"
    )

    assert stderr == ""
    json_content = json.loads(stdout)
    assert isinstance(json_content, list), "Expected a json list"
    assert len(json_content) == 2, "Expected 2 targets"
    assert json_content[0]["id"] == target_id0, "Expected target_id0 in json"
    assert json_content[1]["id"] == target_id1, "Expected target_id1 in json"
