from unittest.mock import patch, Mock

import pytest

from probely_cli.exceptions import ProbelyRequestFailed
from probely_cli.sdk.scans import start_scan


@patch("probely_cli.sdk.scans.RequestProbely.post")
def test_start_scan(mock_client: Mock, valid_scans_start_api_response):
    response_content = valid_scans_start_api_response
    valid_status_code = 200

    target_id_to_be_scanned = valid_scans_start_api_response["target"]["id"]

    mock_client.return_value = (valid_status_code, response_content)
    scan = start_scan(target_id_to_be_scanned)

    mock_client.assert_called_once()
    url_arg = mock_client.call_args[0][0]
    extra_payload_arg = mock_client.call_args[0][1]

    assert target_id_to_be_scanned in url_arg
    assert extra_payload_arg is None
    assert scan == response_content


@patch("probely_cli.sdk.scans.RequestProbely.post")
def test_start_scan_failed(mock_client):
    response_content = {"error": "random error message"}
    invalid_status_code = 400

    mock_client.return_value = (invalid_status_code, response_content)

    with pytest.raises(ProbelyRequestFailed) as exc_info:
        start_scan("random_id")

        assert exc_info == response_content

    mock_client.assert_called_once()
