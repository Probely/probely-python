from typing import Dict
from unittest.mock import patch, Mock

import pytest


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
