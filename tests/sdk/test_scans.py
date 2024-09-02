from typing import Dict
from unittest.mock import patch, Mock

import pytest

from probely_cli.exceptions import ProbelyRequestFailed
from probely_cli.sdk.scans import start_scan, cancel_scans


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
def test_start_scan(mock_client: Mock, valid_scans_start_api_response: Dict):
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


@patch(
    "probely_cli.sdk.client.ProbelyAPIClient.post",
    return_value=(200, {"content": "not relevant"}),
)
def test_start_scan_with_extra_payload(mock_client: Mock):
    random_id = "sdkfjsfhskfjhs"
    extra_payload = {"some_example": "example value"}

    start_scan(random_id, extra_payload)

    mock_client.assert_called_once()

    request_body = mock_client.call_args[0][1]
    assert request_body == extra_payload


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
def test_start_scan_failed(mock_client):
    response_error_content = {"error": "random error message"}
    invalid_status_code = 400

    mock_client.return_value = (invalid_status_code, response_error_content)

    with pytest.raises(ProbelyRequestFailed) as exc_info:
        start_scan("random_id")

        assert exc_info == response_error_content

    mock_client.assert_called_once()


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
def test_cancel_scan(mock_client: Mock, valid_scans_cancel_api_response: Dict):
    response_content = valid_scans_cancel_api_response
    valid_status_code = 200

    scan_id_to_cancel = valid_scans_cancel_api_response["id"]

    mock_client.return_value = (valid_status_code, response_content)
    scan = cancel_scans([scan_id_to_cancel])

    mock_client.assert_called_once()
    scans_to_cancel = mock_client.call_args[0][1]

    assert scans_to_cancel is not None
    assert scans_to_cancel["scans"][0]["id"] == scan_id_to_cancel
    assert scan == response_content


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
def test_cancel_scan_failed(mock_client):
    response_error_content = {"error": "random error message"}
    invalid_status_code = 400

    mock_client.return_value = (invalid_status_code, response_error_content)

    with pytest.raises(ProbelyRequestFailed) as exc_info:
        cancel_scans(["random_id"])

        assert exc_info == response_error_content

    mock_client.assert_called_once()
