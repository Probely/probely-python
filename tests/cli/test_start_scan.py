from typing import Dict
from unittest.mock import patch, Mock

import pytest


@patch("probely_cli.cli.commands.scans.start.start_scan")
def test_start_scans_command_handler(
    sdk_start_scan_mock: Mock,
    valid_scans_start_api_response: Dict,
    cli_parser,
    capsys,
):
    sdk_start_scan_mock.return_value = valid_scans_start_api_response
    args = cli_parser.parse_args(["scans", "start", "random_target_id"])
    args.func(args)

    expected_id = valid_scans_start_api_response["id"]

    captured = capsys.readouterr()
    assert captured.out == expected_id + "\n"
    assert captured.err == ""


# todo: test raw response


@patch("probely_cli.cli.commands.scans.start.start_scan")
def test_start_scans_yaml_file_argument(
    sdk_start_scan_mock: Mock,
    valid_scans_start_api_response: Dict,
    cli_parser,
    capsys,
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
    args = cli_parser.parse_args(
        [
            "scans",
            "start",
            "random_target_id",
            "-f",
            testable_yaml_file_path,
        ]
    )
    args.func(args)

    extra_payload_arg = sdk_start_scan_mock.call_args[0][1]
    assert extra_payload_arg == file_content


@patch("probely_cli.cli.commands.scans.start.start_scan")
def test_start_scans_request_with_exception(
    sdk_start_scan_mock: Mock, cli_parser, capsys
):
    exception_message = "An error occurred"

    sdk_start_scan_mock.side_effect = Exception(exception_message)
    captured = capsys.readouterr()

    with pytest.raises(Exception):
        args = cli_parser.parse_args(["scans", "start", "random_target_id"])
        args.func(args)
        assert captured.out == ""
        assert captured.err == exception_message

    sdk_start_scan_mock.assert_called_once()
