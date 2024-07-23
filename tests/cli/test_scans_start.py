from typing import Dict
from unittest.mock import patch, Mock

import pytest


@patch("probely_cli.cli.commands.scans.start.start_scan")
def test_start_scans_command_handler(
    sdk_start_scan_mock: Mock,
    valid_scans_start_api_response: Dict,
    probely_cli,
):
    sdk_start_scan_mock.return_value = valid_scans_start_api_response
    stdout, stderr = probely_cli("scans", "start", "random_target_id")

    expected_id = valid_scans_start_api_response["id"]

    assert stdout == expected_id + "\n"
    assert stderr == ""


# todo: test raw response


@patch("probely_cli.cli.commands.scans.start.start_scan")
def test_scans_start_yaml_file_argument(
    sdk_start_scan_mock: Mock,
    valid_scans_start_api_response: Dict,
    probely_cli,
    create_testable_yaml_file,
):
    file_content = {
        "key1": "value1",
        "list_key": [
            "item1",
            "item2",
        ],
    }
    testable_yaml_file_path = create_testable_yaml_file(
        file_name="test_start_scans_yaml_file_argument.yaml", file_content=file_content
    )

    sdk_start_scan_mock.return_value = valid_scans_start_api_response

    probely_cli(
        "scans",
        "start",
        "random_target_id",
        "-f",
        testable_yaml_file_path,
    )

    extra_payload_arg = sdk_start_scan_mock.call_args[0][1]
    assert extra_payload_arg == file_content


@patch("probely_cli.cli.commands.scans.start.start_scan")
def test_scans_start_request_with_exception(
    sdk_start_scan_mock: Mock,
    probely_cli,
):
    exception_message = "An error occurred"

    sdk_start_scan_mock.side_effect = Exception(exception_message)

    with pytest.raises(Exception):
        stdout, stderr = probely_cli("scans", "start", "random_target_id")
        assert stdout == ""
        assert stderr == exception_message

    sdk_start_scan_mock.assert_called_once()
