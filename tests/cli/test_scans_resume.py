from typing import Dict
from unittest.mock import patch, Mock

import pytest


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
    assert valid_scans_resume_api_response["id"] == stdout_lines[0]
    assert resp2["id"] == stdout_lines[1]


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
    assert len(stdout_lines) == 1, "Expected to have 1 line with the resumed scan id"
    assert scan_id1 == stdout_lines[0]


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
    assert len(stdout_lines) == 1, "Expected to have 1 line with the resumed scan id"
    assert scan_id1 == stdout_lines[0]


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
