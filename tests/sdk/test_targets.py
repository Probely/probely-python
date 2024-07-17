import json
from unittest.mock import Mock, patch

import pytest

from probely_cli.exceptions import ProbelyRequestFailed
from probely_cli.sdk.targets import get_targets


@patch("probely_cli.sdk.client.ProbelyAPIClient.get")
def test_list_targets_ok(api_client_mock: Mock):
    expected_content = [{"list": "of objects1"}, {"list": "of objects2"}]
    response_content = {"results": expected_content}

    api_client_mock.return_value = (200, response_content)

    r = get_targets()
    assert r == expected_content


@patch("probely_cli.sdk.client.ProbelyAPIClient.get")
def test_list_targets_unsuccessful(api_client_mock: Mock):
    invalid_status_code = 400
    error_message = "request invalid"
    error_response_content = {"detail": error_message}

    api_client_mock.return_value = (invalid_status_code, error_response_content)

    with pytest.raises(ProbelyRequestFailed) as exc:
        get_targets()

        raised_exception = exc.value
        assert str(raised_exception) == error_message
