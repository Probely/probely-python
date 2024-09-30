from unittest.mock import Mock, patch

import pytest

from probely.exceptions import ProbelyRequestFailed
from probely.sdk.findings import list_findings


@patch("probely.sdk.client.ProbelyAPIClient.get")
def test_list_findings__ok(api_client_mock: Mock):
    expected_content = [{"list": "of objects1"}, {"list": "of objects2"}]
    response_content = {"results": expected_content, "page_total": 1}

    api_client_mock.return_value = (200, response_content)

    r = list(list_findings())
    assert r == expected_content


@patch("probely.sdk.client.ProbelyAPIClient.get")
def test_list_findings__unsuccessful(api_client_mock: Mock):
    invalid_status_code = 400
    error_message = "request invalid"
    error_response_content = {"detail": error_message}

    api_client_mock.return_value = (invalid_status_code, error_response_content)

    with pytest.raises(ProbelyRequestFailed) as exc:
        list(list_findings())

        raised_exception = exc.value
        assert str(raised_exception) == error_message
