import json
from typing import Dict
from unittest.mock import patch, Mock, MagicMock

import pytest
import yaml

from tests.testable_api_responses import PAUSE_SCAN_200_RESPONSE


@patch("probely_cli.cli.commands.scans.pause.pause_scans")
def test_pause_scans__command_handler(
    sdk_pause_scan_mock: Mock,
    valid_scans_pause_api_response: Dict,
    probely_cli,
):
    resp2 = {**valid_scans_pause_api_response, "id": "random_id"}
    sdk_pause_scan_mock.return_value = [valid_scans_pause_api_response, resp2]
    stdout_lines, stderr_lines = probely_cli(
        "scans",
        "pause",
        valid_scans_pause_api_response["id"],
        resp2["id"],
        return_list=True,
    )

    assert len(stderr_lines) == 0
    assert valid_scans_pause_api_response["id"] == stdout_lines[0]
    assert resp2["id"] == stdout_lines[1]


@patch("probely_cli.cli.commands.scans.pause.pause_scans")
@patch("probely_cli.cli.commands.scans.pause.pause_scan")
def test_pause_single_scan__command_handler(
    sdk_pause_scan_mock: Mock,
    sdk_pause_scans_mock: Mock,
    valid_scans_pause_api_response: Dict,
    probely_cli,
):
    sdk_pause_scan_mock.return_value = valid_scans_pause_api_response
    stdout_lines, stderr_lines = probely_cli(
        "scans",
        "pause",
        valid_scans_pause_api_response["id"],
        return_list=True,
    )
    sdk_pause_scan_mock.assert_called()
    sdk_pause_scans_mock.assert_not_called()

    assert len(stderr_lines) == 0
    assert valid_scans_pause_api_response["id"] == stdout_lines[0]


@patch("probely_cli.cli.commands.scans.pause.pause_scan")
def test_scans_pause_request_with_exception(
    sdk_pause_scan_mock: Mock,
    probely_cli,
):
    exception_message = "An error occurred"

    sdk_pause_scan_mock.side_effect = Exception(exception_message)

    with pytest.raises(Exception):
        stdout, stderr = probely_cli(
            "scans",
            "pause",
            "random_scan_id",
        )
        assert stdout == ""
        assert stderr == exception_message

    sdk_pause_scan_mock.assert_called_once()


def test_scans_pause__mutually_exclusive_arguments(probely_cli):
    stdout_lines, stderr_lines = probely_cli(
        "scans",
        "pause",
        "scan_id1 scan_id2",
        "--f-search=test",
        return_list=True,
    )

    assert len(stdout_lines) == 0, "Expected no output"
    assert len(stderr_lines) == 1, "Expected error output"

    assert stderr_lines[-1] == (
        "probely scans pause: error: Filters and Scan IDs are mutually exclusive"
    )


def test_scans_pause__without_any_argument(probely_cli):
    stdout_lines, stderr_lines = probely_cli(
        "scans",
        "pause",
        return_list=True,
    )
    assert len(stdout_lines) == 0, "Expected no output"
    assert len(stderr_lines) == 1, "Expected error output"

    assert stderr_lines[-1] == (
        "probely scans pause: error: Expected scan_ids or filters"
    )


@patch("probely_cli.cli.commands.scans.pause.pause_scan")
@patch("probely_cli.cli.commands.scans.pause.list_scans")
def test_scans_pause_scans_with_filters(
    list_scans_mock: Mock,
    pause_scan_mock: Mock,
    valid_scans_pause_api_response,
    probely_cli,
):
    scan_id1 = valid_scans_pause_api_response["id"]
    list_scans_mock.return_value = [{"id": scan_id1}]

    pause_scan_mock.return_value = valid_scans_pause_api_response

    stdout_lines, stderr_lines = probely_cli(
        "scans",
        "pause",
        "--f-search=test",
        return_list=True,
    )
    list_scans_mock.assert_called_with(scans_filters={"search": "test"})
    pause_scan_mock.assert_called_once_with(scan_id1)
    assert len(stderr_lines) == 0
    assert len(stdout_lines) == 1, "Expected to have 1 line with the resumed scan id"
    assert scan_id1 == stdout_lines[0]


@patch("probely_cli.cli.commands.scans.pause.pause_scan")
@patch("probely_cli.cli.commands.scans.pause.pause_scans")
@patch("probely_cli.cli.commands.scans.pause.list_scans")
def test_scans_pause__filters_with_no_results(
    sdk_list_scans_mock: MagicMock,
    pause_scans_mock: MagicMock,
    pause_scan_mock: MagicMock,
    probely_cli,
):

    sdk_list_scans_mock.return_value = []

    stdout_lines, stderr_lines = probely_cli(
        "scans",
        "pause",
        "--f-search=test",
        return_list=True,
    )

    assert stdout_lines == [], "Expected no output"
    assert len(stderr_lines) == 1, "Expected error output"

    expected_error = "probely scans pause: error: Selected Filters returned no results"
    assert stderr_lines[-1] == expected_error

    pause_scans_mock.assert_not_called()
    pause_scan_mock.assert_not_called()


@patch("probely_cli.cli.commands.scans.pause.pause_scans")
def test_scans_pause__output_argument_output(pause_scans_mock, probely_cli):
    scan_id0 = "scan_id0"
    scan_id1 = "scan_id1"

    scan_id1_content = PAUSE_SCAN_200_RESPONSE.copy()
    scan_id2_content = PAUSE_SCAN_200_RESPONSE.copy()

    scan_id1_content["id"] = scan_id0
    scan_id2_content["id"] = scan_id1

    pause_scans_mock.return_value = [scan_id1_content, scan_id2_content]

    stdout, _ = probely_cli(
        "scans",
        "pause",
        scan_id0,
        scan_id1,
    )

    stdout, stderr = probely_cli("scans", "pause", scan_id0, scan_id1, "-o yaml")

    assert stderr == ""
    yaml_content = yaml.load(stdout, Loader=yaml.FullLoader)
    assert isinstance(yaml_content, list), "Expected a yaml list"
    assert len(yaml_content) == 2, "Expected 2 scans"
    assert yaml_content[0]["id"] == scan_id0, "Expected scan_id0 in yaml content"
    assert yaml_content[1]["id"] == scan_id1, "Expected scan_id1 in yaml content"

    stdout, stderr = probely_cli("scans", "pause", scan_id0, scan_id1, "--output json")

    assert stderr == ""
    json_content = json.loads(stdout)
    assert isinstance(json_content, list), "Expected a json list"
    assert len(json_content) == 2, "Expected 2 scans"
    assert json_content[0]["id"] == scan_id0, "Expected scan_id0 in json"
    assert json_content[1]["id"] == scan_id1, "Expected scan_id1 in json"
