from typing import Dict
from unittest.mock import patch, Mock

import pytest

from probely_cli.cli.common import ScanStatusEnum


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
    assert valid_scans_cancel_api_response["id"] == stdout_lines[0]
    assert resp2["id"] == stdout_lines[1]


@patch("probely_cli.cli.commands.scans.cancel.cancel_scans")
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
            "random_target_id",
        )
        assert stdout == ""
        assert stderr == exception_message

    sdk_cancel_scan_mock.assert_called_once()


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

    assert stderr_lines[0] == (
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
