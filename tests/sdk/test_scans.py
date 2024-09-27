from typing import Dict
from unittest.mock import Mock, patch

import pytest

from probely_cli.exceptions import (
    ProbelyBadRequest,
    ProbelyObjectNotFound,
    ProbelyRequestFailed,
)
from probely_cli.sdk.scans import (
    cancel_scans,
    list_scans,
    pause_scan,
    pause_scans,
    resume_scans,
    start_scan,
    start_scans,
)
from probely_cli.settings import (
    PROBELY_API_SCANS_BULK_START_URL,
    PROBELY_API_TARGETS_START_SCAN_URL,
)


@pytest.mark.parametrize(
    "payload",
    [
        None,
        {"key": "value"},
    ],
)
@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
def test_start_scan(
    api_client_mock: Mock,
    valid_scans_start_api_response: Dict,
    payload,
):
    """
    Test that start_scan successfully starts a scan and returns the scan details,
    both with and without an extra payload.
    """
    target_id = valid_scans_start_api_response["target"]["id"]
    expected_response = valid_scans_start_api_response
    expected_endpoint_url = PROBELY_API_TARGETS_START_SCAN_URL.format(
        target_id=target_id
    )

    api_client_mock.return_value = (200, expected_response)

    result = start_scan(target_id, payload)

    assert result == expected_response
    api_client_mock.assert_called_once_with(expected_endpoint_url, payload=payload)


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
def test_start_scan_failed(api_client_mock: Mock):
    # Ensure ProbelyBadRequest is raised if API returns status code 400
    api_validation_error = {"error": "A scan is already in progress for this target."}
    api_client_mock.return_value = (400, api_validation_error)

    with pytest.raises(ProbelyBadRequest) as exc_info:
        start_scan("random_id")
        assert exc_info == api_validation_error

    # Ensure ProbelyObjectNotFound is raised if API returns status code 404
    api_client_mock.return_value = (404, {})
    with pytest.raises(ProbelyObjectNotFound) as exc_info:
        start_scan("invalid_target_id")
        assert exc_info.value.not_found_object_id == "invalid_target_id"

    # Ensure ProbelyRequestFailed is raised if API returns some another notok status code
    api_error = {"detail": "Incorrect authentication credentials."}
    api_client_mock.return_value = (401, api_error)
    with pytest.raises(ProbelyRequestFailed) as exc_info:
        start_scan("random_id")
        assert exc_info.value.reason == api_error


@patch("probely_cli.sdk.scans.ProbelyAPIClient.post")
@patch("probely_cli.sdk.scans.validate_resource_ids")
def test_start_scans__successful_api_call(
    validate_resource_ids_mock: Mock,
    api_client_mock: Mock,
    valid_scans_start_api_response: Dict,
):
    validate_resource_ids_mock.return_value = None  # target IDs are valid
    expected_endpoint_url = PROBELY_API_SCANS_BULK_START_URL
    payload = {"overrides": {"scan_profile": "lightning"}}
    target_ids = ["target_id1", "target_id2"]
    expected_payload_on_api_call = {
        "targets": [{"id": target_id} for target_id in target_ids],
        **payload,
    }
    expected_response = [valid_scans_start_api_response for _ in target_ids]

    api_client_mock.return_value = (200, expected_response)
    result = start_scans(target_ids, payload)

    assert result == expected_response
    api_client_mock.assert_called_once_with(
        expected_endpoint_url, payload=expected_payload_on_api_call
    )


@patch("probely_cli.sdk.scans.ProbelyAPIClient.post")
@patch("probely_cli.sdk.scans.validate_resource_ids")
def test_start_scans__unsuccessful_api_call(
    validate_resource_ids_mock: Mock, api_client_mock: Mock
):
    # Ensure ProbelyObjectNotFound is raised if invalid target IDs are provided:
    scanned_target_ids = ["invalid_id1"]
    validate_resource_ids_mock.side_effect = ProbelyObjectNotFound(
        id=scanned_target_ids[0]
    )

    with pytest.raises(ProbelyObjectNotFound) as exc_info:
        start_scans(scanned_target_ids)
        assert exc_info.value.not_found_object_id == scanned_target_ids[0]

    # Ensure ProbelyBadRequest is raised if API returns status code 400
    validate_resource_ids_mock.side_effect = None
    validate_resource_ids_mock.returne_value = (
        None  # Target IDs are valid for this scenario
    )

    api_validation_error = {"error": "Invalid scan profile"}
    api_client_mock.return_value = (400, api_validation_error)

    with pytest.raises(ProbelyBadRequest) as exc_info:
        start_scans(["target_id1", "target_id2"])
        assert exc_info == api_validation_error

    # Ensure ProbelyRequestFailed is raised if API returns some another notok status code
    api_error = {"detail": "Incorrect authentication credentials."}
    api_client_mock.return_value = (401, api_error)
    with pytest.raises(ProbelyRequestFailed) as exc_info:
        start_scans(["random_id", "another_random_id"])
        assert exc_info.value.reason == api_error


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
@patch("probely_cli.sdk.scans.retrieve_scan")
def test_cancel_scan(
    sdk_retrieve_scan_mock: Mock,
    mock_client: Mock,
    valid_scans_cancel_api_response: Dict,
):
    response_content = valid_scans_cancel_api_response
    sdk_retrieve_scan_mock.return_value = valid_scans_cancel_api_response

    valid_status_code = 200

    scan_id_to_cancel = valid_scans_cancel_api_response["id"]

    mock_client.return_value = (valid_status_code, response_content)
    scan = cancel_scans([scan_id_to_cancel])

    mock_client.assert_called_once()
    _args, kwargs = mock_client.call_args

    scans_to_cancel = kwargs["payload"]

    assert scans_to_cancel is not None
    assert scans_to_cancel["scans"][0]["id"] == scan_id_to_cancel
    assert scan == [response_content]


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
@patch("probely_cli.sdk.scans.retrieve_scan")
def test_cancel_scan_failed(
    sdk_retrieve_scan_mock: Mock, mock_client, valid_scans_cancel_api_response
):
    response_error_content = {"error": "random error message"}
    invalid_status_code = 400
    sdk_retrieve_scan_mock.return_value = valid_scans_cancel_api_response

    mock_client.return_value = (invalid_status_code, response_error_content)

    with pytest.raises(ProbelyRequestFailed) as exc_info:
        cancel_scans(["random_id"])

        assert exc_info == response_error_content

    mock_client.assert_called_once()


@patch("probely_cli.sdk.client.ProbelyAPIClient.get")
def test_list_scans__ok(api_client_mock: Mock):
    expected_content = [{"id": "scan1"}, {"id": "scan2"}]
    response_content = {"results": expected_content, "page_total": 1}

    api_client_mock.return_value = (200, response_content)

    r = list(list_scans())
    assert r == expected_content


@patch("probely_cli.sdk.client.ProbelyAPIClient.get")
def test_list_scans__notok(api_client_mock: Mock):
    invalid_status_code = 400
    error_message = "request invalid"
    error_response_content = {"detail": error_message}

    api_client_mock.return_value = (invalid_status_code, error_response_content)

    with pytest.raises(ProbelyRequestFailed) as exc:
        list(list_scans())
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
    _args, kwargs = mock_client.call_args

    scans_to_resume = kwargs["payload"]

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
    _args, kwargs = mock_client.call_args

    scans_to_pause = kwargs["payload"]

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
