from typing import Dict
from unittest.mock import patch, Mock

import pytest

from probely_cli.exceptions import ProbelyObjectNotFound, ProbelyRequestFailed
from probely_cli.sdk.scans import (
    list_scans,
    pause_scan,
    pause_scans,
    resume_scans,
    start_scan,
    cancel_scans,
)


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


@patch("probely_cli.sdk.client.ProbelyAPIClient.get")
def test_list_scans__ok(api_client_mock: Mock):
    expected_content = [{"id": "scan1"}, {"id": "scan2"}]
    response_content = {"results": expected_content}

    api_client_mock.return_value = (200, response_content)

    r = list_scans()
    assert r == expected_content


@patch("probely_cli.sdk.client.ProbelyAPIClient.get")
def test_list_scans__notok(api_client_mock: Mock):
    invalid_status_code = 400
    error_message = "request invalid"
    error_response_content = {"detail": error_message}

    api_client_mock.return_value = (invalid_status_code, error_response_content)

    with pytest.raises(ProbelyRequestFailed) as exc:
        list_scans()
        raised_exception = exc.value
        assert str(raised_exception) == error_message


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
@patch("probely_cli.sdk.scans.retrieve_scan")
def test_resume_scan(
    sdk_retrieve_scan_mock: Mock,
    mock_client: Mock,
    valid_scans_resume_api_response: Dict,
):
    response_content = valid_scans_resume_api_response
    valid_status_code = 200

    sdk_retrieve_scan_mock.return_value = valid_scans_resume_api_response

    scan_id_to_resume = valid_scans_resume_api_response["id"]

    mock_client.return_value = (valid_status_code, response_content)
    scan = resume_scans([scan_id_to_resume])

    mock_client.assert_called_once()
    scans_to_resume = mock_client.call_args[0][1]

    assert scans_to_resume is not None
    assert scans_to_resume["scans"][0]["id"] == scan_id_to_resume
    assert scan == [response_content]


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
@patch("probely_cli.sdk.scans.retrieve_scan")
def test_resume_scan_failed(
    sdk_retrieve_scan_mock: Mock, mock_client, valid_scans_resume_api_response
):
    response_error_content = {"error": "random error message"}
    invalid_status_code = 400
    sdk_retrieve_scan_mock.return_value = valid_scans_resume_api_response
    mock_client.return_value = (invalid_status_code, response_error_content)

    with pytest.raises(ProbelyRequestFailed) as exc_info:
        resume_scans(["random_id"])
        assert exc_info == response_error_content

    mock_client.assert_called_once()


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
@patch("probely_cli.sdk.scans.retrieve_scan")
def test_resume_scan_failed_invalid_ids(
    sdk_retrieve_scan_mock: Mock, mock_client: Mock
):

    scan_id = "random_scan_id"
    exception_message = f"probely scans resume: error: objects '{scan_id}' not found.\n"
    sdk_retrieve_scan_mock.side_effect = ProbelyObjectNotFound(exception_message)
    with pytest.raises(ProbelyObjectNotFound) as exc_info:
        resume_scans([scan_id])

        assert exc_info == exception_message

    mock_client.assert_not_called()


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
@patch("probely_cli.sdk.scans.retrieve_scan")
def test_pause_scans(
    sdk_retrieve_scan_mock: Mock,
    mock_client: Mock,
    valid_scans_pause_api_response: Dict,
):
    sdk_retrieve_scan_mock.return_value = valid_scans_pause_api_response

    response_content = valid_scans_pause_api_response
    valid_status_code = 200

    scan_id_to_pause = valid_scans_pause_api_response["id"]

    mock_client.return_value = (valid_status_code, response_content)
    scan = pause_scans([scan_id_to_pause])

    mock_client.assert_called_once()
    scans_to_pause = mock_client.call_args[0][1]

    assert scans_to_pause is not None
    assert scans_to_pause["scans"][0]["id"] == scan_id_to_pause
    assert scan == [response_content]


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
@patch("probely_cli.sdk.scans.retrieve_scan")
def test_pause_scans_failed(
    sdk_retrieve_scan_mock: Mock, mock_client, valid_scans_pause_api_response
):
    response_error_content = {"error": "random error message"}
    invalid_status_code = 400

    sdk_retrieve_scan_mock.return_value = valid_scans_pause_api_response

    mock_client.return_value = (invalid_status_code, response_error_content)

    with pytest.raises(ProbelyRequestFailed) as exc_info:
        pause_scans(["random_id"])

        assert exc_info == response_error_content

    mock_client.assert_called_once()


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
@patch("probely_cli.sdk.scans.retrieve_scan")
def test_pause_scans_failed_invalid_ids(
    sdk_retrieve_scan_mock: Mock, mock_client: Mock
):
    scan_id = "random_scan_id"
    exception_message = f"probely scans cancel: error: objects '{scan_id}' not found.\n"
    sdk_retrieve_scan_mock.side_effect = ProbelyObjectNotFound(exception_message)
    with pytest.raises(ProbelyObjectNotFound) as exc_info:
        pause_scans([scan_id])

        assert exc_info == exception_message

    mock_client.assert_not_called()


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
@patch("probely_cli.sdk.scans.retrieve_scan")
def test_pause_scan(
    sdk_retrieve_scan_mock: Mock,
    mock_client: Mock,
    valid_scans_pause_api_response: Dict,
):
    sdk_retrieve_scan_mock.return_value = valid_scans_pause_api_response

    response_content = valid_scans_pause_api_response
    valid_status_code = 200

    scan_id_to_pause = valid_scans_pause_api_response["id"]

    mock_client.return_value = (valid_status_code, response_content)
    scan = pause_scan(scan_id_to_pause)

    mock_client.assert_called_once()
    assert scan == response_content


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
@patch("probely_cli.sdk.scans.retrieve_scan")
def test_pause_scans_failed(
    sdk_retrieve_scan_mock: Mock, mock_client, valid_scans_pause_api_response
):
    response_error_content = {"error": "random error message"}
    invalid_status_code = 400

    sdk_retrieve_scan_mock.return_value = valid_scans_pause_api_response

    mock_client.return_value = (invalid_status_code, response_error_content)

    with pytest.raises(ProbelyRequestFailed) as exc_info:
        pause_scan(["random_id"])

        assert exc_info == response_error_content

    mock_client.assert_called_once()
