import json
from typing import Dict
from unittest.mock import patch, Mock

import pytest
import yaml

from probely_cli.sdk.common import ScanStatusEnum


@patch("probely_cli.cli.commands.scans.cancel.cancel_scans")
def test_cancel_scans__command_handler(
    sdk_cancel_scan_mock: Mock,
    valid_scans_cancel_api_response: Dict,
    probely_cli,
):
    resp2 = {**valid_scans_cancel_api_response, "id": "random_id"}
    sdk_cancel_scan_mock.return_value = [valid_scans_cancel_api_response, resp2]
    stdout_lines, stderr_lines = probely_cli(
        "scans",
        "cancel",
        valid_scans_cancel_api_response["id"],
        resp2["id"],
        return_list=True,
    )

    assert len(stderr_lines) == 0
    assert valid_scans_cancel_api_response["id"] in stdout_lines
    assert resp2["id"] in stdout_lines


@patch("probely_cli.cli.commands.scans.cancel.cancel_scan")
def test_scans_cancel_request_with_exception(
    sdk_cancel_scan_mock: Mock,
    probely_cli,
):
    exception_message = "An error occurred"

    sdk_cancel_scan_mock.side_effect = Exception(exception_message)

    with pytest.raises(Exception):
        stdout, stderr = probely_cli(
            "scans",
            "cancel",
            "random_scan_id",
        )
        assert stdout == ""
        assert stderr == exception_message

    sdk_cancel_scan_mock.assert_called_once()

    assert stdout == "", f"Expected no output, but got: {stdout}"
    assert stderr == f"probely scans cancel: error: {exception_message}\n"


def test_scans_cancel__mutually_exclusive_arguments(probely_cli):
    stdout_lines, stderr_lines = probely_cli(
        "scans",
        "cancel",
        "scan_id1 scan_id2",
        "--f-search=test",
        return_list=True,
    )
    assert len(stdout_lines) == 0, "Expected no output"
    assert len(stderr_lines) == 1, "Expected error output"

    assert stderr_lines[-1] == (
        "probely scans cancel: error: Filters and Scan IDs are mutually exclusive"
    )


def test_scans_cancel__no_arguments_passed(probely_cli):
    stdout_lines, stderr_lines = probely_cli(
        "scans",
        "cancel",
        return_list=True,
    )
    assert len(stdout_lines) == 0, "Expected no output"
    assert len(stderr_lines) == 1, "Expected error output"

    assert stderr_lines[-1] == (
        "probely scans cancel: error: Expected scan_ids or filters"
    )


@pytest.mark.parametrize(
    "filter_arg, expected_filter_request",
    [
        ("--f-search=meh", {"search": "meh"}),
        ("--f-search meh", {"search": "meh"}),
        (
            "--f-status PAUSING STARTED",
            {
                "status": [
                    ScanStatusEnum.PAUSING.api_filter_value,
                    ScanStatusEnum.STARTED.api_filter_value,
                ]
            },
        ),
    ],
)
@patch("probely_cli.cli.commands.scans.get.list_scans")
def test_scans_cancel__arg_filters_success(
    sdk_list_scans_mock: Mock,
    filter_arg,
    expected_filter_request,
    probely_cli,
):
    stdout, stderr = probely_cli("scans", "get", filter_arg, return_list=True)

    assert len(stderr) == 0, "Expected no errors"
    sdk_list_scans_mock.assert_called_once_with(scans_filters=expected_filter_request)


@patch("probely_cli.cli.commands.scans.cancel.cancel_scans")
def test_scans_cancel__output_argument_output(
    cancel_scans_mock, valid_scans_cancel_api_response: dict, probely_cli
):
    scan_id0 = "scan_id0"
    scan_id1 = "scan_id1"

    scan_id1_content = valid_scans_cancel_api_response.copy()
    scan_id2_content = valid_scans_cancel_api_response.copy()

    scan_id1_content["id"] = scan_id0
    scan_id2_content["id"] = scan_id1

    cancel_scans_mock.return_value = [scan_id1_content, scan_id2_content]

    stdout, _ = probely_cli(
        "scans",
        "cancel",
        scan_id0,
        scan_id1,
    )

    stdout, stderr = probely_cli("scans", "cancel", scan_id0, scan_id1, "-o yaml")

    assert stderr == ""
    yaml_content = yaml.load(stdout, Loader=yaml.FullLoader)
    assert isinstance(yaml_content, list), "Expected a yaml list"
    assert len(yaml_content) == 2, "Expected 2 scans"
    assert yaml_content[0]["id"] == scan_id0, "Expected scan_id0 in yaml content"
    assert yaml_content[1]["id"] == scan_id1, "Expected scan_id1 in yaml content"

    stdout, stderr = probely_cli("scans", "cancel", scan_id0, scan_id1, "--output json")

    assert stderr == ""
    json_content = json.loads(stdout)
    assert isinstance(json_content, list), "Expected a json list"
    assert len(json_content) == 2, "Expected 2 scans"
    assert json_content[0]["id"] == scan_id0, "Expected scan_id0 in json"
    assert json_content[1]["id"] == scan_id1, "Expected scan_id1 in json"


@patch("probely_cli.cli.commands.scans.cancel.cancel_scans")
@patch("probely_cli.cli.commands.scans.cancel.cancel_scan")
def test_cancel_single_scan__command_handler(
    sdk_cancel_scan_mock: Mock,
    sdk_cancel_scans_mock: Mock,
    valid_scans_cancel_api_response: Dict,
    probely_cli,
):
    sdk_cancel_scan_mock.return_value = valid_scans_cancel_api_response
    stdout_lines, stderr_lines = probely_cli(
        "scans",
        "cancel",
        valid_scans_cancel_api_response["id"],
        return_list=True,
    )
    sdk_cancel_scan_mock.assert_called()
    sdk_cancel_scans_mock.assert_not_called()

    assert len(stderr_lines) == 0
    assert valid_scans_cancel_api_response["id"] == stdout_lines[0]
