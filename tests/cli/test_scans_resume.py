import json
from typing import Dict
from unittest.mock import patch, Mock

import pytest
import yaml


@patch("probely_cli.cli.commands.scans.resume.resume_scans")
def test_resume_scans__command_handler(
    sdk_resume_scan_mock: Mock,
    valid_scans_resume_api_response: Dict,
    probely_cli,
):
    resp2 = {**valid_scans_resume_api_response, "id": "random_id"}

    sdk_resume_scan_mock.return_value = [valid_scans_resume_api_response, resp2]
    stdout_lines, stderr_lines = probely_cli(
        "scans",
        "resume",
        valid_scans_resume_api_response["id"],
        resp2["id"],
        return_list=True,
    )

    assert len(stderr_lines) == 0
    assert valid_scans_resume_api_response["id"] in stdout_lines
    assert resp2["id"] in stdout_lines


@patch("probely_cli.cli.commands.scans.resume.resume_scans")
def test_scans_resume_request_with_exception(
    sdk_resume_scan_mock: Mock,
    probely_cli,
):
    exception_message = "An error occurred"

    sdk_resume_scan_mock.side_effect = Exception(exception_message)

    with pytest.raises(Exception):
        stdout, stderr = probely_cli(
            "scans",
            "resume",
            "random_scan_id",
        )
        assert stdout == ""
        assert stderr == exception_message

    sdk_resume_scan_mock.assert_called_once()


@patch("probely_cli.cli.commands.scans.resume.resume_scans")
@patch("probely_cli.cli.commands.scans.resume.list_scans")
def test_scans_resume_scans_with_filters(
    list_scans_mock: Mock,
    resume_scans_mock: Mock,
    valid_scans_resume_api_response,
    probely_cli,
):
    scan_id1 = valid_scans_resume_api_response["id"]
    list_scans_mock.return_value = [{"id": scan_id1}]

    resume_scans_mock.return_value = [valid_scans_resume_api_response]

    stdout_lines, stderr_lines = probely_cli(
        "scans",
        "resume",
        "--f-search=test",
        return_list=True,
    )

    list_scans_mock.assert_called_with(scans_filters={"search": "test"})
    resume_scans_mock.assert_called_once_with([scan_id1], ignore_blackout_period=False)
    assert len(stderr_lines) == 0
    assert len(stdout_lines) == 1, "Expected to have 1 item in data"
    assert scan_id1 in stdout_lines


@patch("probely_cli.cli.commands.scans.resume.resume_scans")
def test_scans_resume_scans_with_ignore_blackout(
    resume_scans_mock: Mock,
    valid_scans_resume_api_response,
    probely_cli,
):
    scan_id1 = valid_scans_resume_api_response["id"]

    resume_scans_mock.return_value = [valid_scans_resume_api_response]

    stdout_lines, stderr_lines = probely_cli(
        "scans",
        "resume",
        scan_id1,
        "--ignore-blackout-period",
        return_list=True,
    )
    resume_scans_mock.assert_called_once_with([scan_id1], ignore_blackout_period=True)
    assert len(stderr_lines) == 0
    assert len(stdout_lines) == 1, "Expected to have 1 item in data"
    assert scan_id1 in stdout_lines


def test_scans_resume__mutually_exclusive_arguments(probely_cli):
    stdout_lines, stderr_lines = probely_cli(
        "scans",
        "resume",
        "scan_id1 scan_id2",
        "--f-search=test",
        return_list=True,
    )

    assert len(stdout_lines) == 0, "Expected no output"
    assert len(stderr_lines) == 1, "Expected error output"

    assert stderr_lines[-1] == (
        "probely scans resume: error: Filters and Scan IDs are mutually exclusive"
    )


def test_scans_resume__without_any_argument(probely_cli):
    stdout_lines, stderr_lines = probely_cli(
        "scans",
        "resume",
        return_list=True,
    )
    assert len(stdout_lines) == 0, "Expected no output"
    assert len(stderr_lines) == 1, "Expected error output"

    assert stderr_lines[-1] == (
        "probely scans resume: error: Expected scan_ids or filters"
    )


@patch("probely_cli.cli.commands.scans.resume.resume_scans")
def test_scans_resume__output_argument_output(
    resume_scans_mock, valid_scans_resume_api_response: dict, probely_cli
):
    scan_id0 = "scan_id0"
    scan_id1 = "scan_id1"

    scan_id1_content = valid_scans_resume_api_response.copy()
    scan_id2_content = valid_scans_resume_api_response.copy()

    scan_id1_content["id"] = scan_id0
    scan_id2_content["id"] = scan_id1

    resume_scans_mock.return_value = [scan_id1_content, scan_id2_content]

    stdout, _ = probely_cli(
        "scans",
        "resume",
        scan_id0,
        scan_id1,
    )

    stdout, stderr = probely_cli("scans", "resume", scan_id0, scan_id1, "-o yaml")

    assert stderr == ""
    yaml_content = yaml.load(stdout, Loader=yaml.FullLoader)
    assert isinstance(yaml_content, list), "Expected a yaml list"
    assert len(yaml_content) == 2, "Expected 2 scans"
    assert yaml_content[0]["id"] == scan_id0, "Expected scan_id0 in yaml content"
    assert yaml_content[1]["id"] == scan_id1, "Expected scan_id1 in yaml content"

    stdout, stderr = probely_cli("scans", "resume", scan_id0, scan_id1, "--output json")

    assert stderr == ""
    json_content = json.loads(stdout)
    assert isinstance(json_content, list), "Expected a json list"
    assert len(json_content) == 2, "Expected 2 scans"
    assert json_content[0]["id"] == scan_id0, "Expected scan_id0 in json"
    assert json_content[1]["id"] == scan_id1, "Expected scan_id1 in json"
