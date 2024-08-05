from unittest.mock import Mock, patch

import pytest

from probely_cli.exceptions import ProbelyRequestFailed
from probely_cli.sdk.targets import list_targets


@patch("probely_cli.sdk.client.ProbelyAPIClient.get")
def test_list_targets__ok(api_client_mock: Mock):
    expected_content = [{"list": "of objects1"}, {"list": "of objects2"}]
    response_content = {"results": expected_content}

    api_client_mock.return_value = (200, response_content)

    r = list_targets()
    assert r == expected_content


@patch("probely_cli.sdk.client.ProbelyAPIClient.get")
def test_list_targets__unsuccessful(api_client_mock: Mock):
    invalid_status_code = 400
    error_message = "request invalid"
    error_response_content = {"detail": error_message}

    api_client_mock.return_value = (invalid_status_code, error_response_content)

    with pytest.raises(ProbelyRequestFailed) as exc:
        list_targets()

        raised_exception = exc.value
        assert str(raised_exception) == error_message


@patch("probely_cli.sdk.client.ProbelyAPIClient.get")
def test_list_targets__filters(api_client_mock: Mock):
    resp_code = 200  # random
    resp_content = {"results": "content"}  # random

    api_client_mock.return_value = (resp_code, resp_content)

    expected_filter_key = "filter1"
    filters = {expected_filter_key: "value1"}
    list_targets(targets_filters=filters)

    query_params_args = api_client_mock.call_args[1]["query_params"]

    assert (
        expected_filter_key in query_params_args
    ), "Filters should be inject in the request as query params"
