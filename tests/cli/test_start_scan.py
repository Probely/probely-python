from unittest.mock import patch, Mock

import pytest


@patch("probely_cli.cli.commands.scans.start.start_scan")
def test_start_scans_command_handler(sdk_start_scan_mock, cli_parser, capsys):
    sdk_start_scan_mock.return_value = {
        "id": "random_target_id"
    }  # todo: find real output to use as example
    args = cli_parser.parse_args(["scans", "start", "random_target_id"])
    args.func(args)

    captured = capsys.readouterr()
    assert captured.out == "random_target_id\n"
    assert captured.err == ""


# todo: test raw response


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
