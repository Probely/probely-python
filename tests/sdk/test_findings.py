from unittest.mock import Mock, patch

import pytest

from probely.exceptions import ProbelyRequestFailed
from probely.sdk.managers import FindingManager
from probely.sdk.models import Finding
from probely.sdk._schemas import Finding as FindingDataModel


@patch("probely.sdk.client.ProbelyAPIClient.get")
def test_list_findings__ok(
    api_client_mock: Mock,
    valid_get_findings_api_response: dict,
):
    response_content = valid_get_findings_api_response
    expected_content = [
        Finding(FindingDataModel(**finding)) for finding in response_content["results"]
    ]

    api_client_mock.return_value = (200, response_content)

    findings = list(FindingManager().list())
    for i, finding in enumerate(findings):
        assert finding._data == expected_content[i]._data


@patch("probely.sdk.client.ProbelyAPIClient.get")
def test_list_findings__unsuccessful(api_client_mock: Mock):
    invalid_status_code = 400
    error_message = "request invalid"
    error_response_content = {"detail": error_message}

    api_client_mock.return_value = (invalid_status_code, error_response_content)

    with pytest.raises(ProbelyRequestFailed) as exc:
        list(FindingManager().list())

        raised_exception = exc.value
        assert str(raised_exception) == error_message
