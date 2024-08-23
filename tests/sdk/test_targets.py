from unittest.mock import Mock, patch

import pytest

from probely_cli.exceptions import ProbelyRequestFailed, ProbelyObjectNotFound
from probely_cli.sdk.targets import list_targets, retrieve_target, retrieve_targets
from probely_cli.settings import PROBELY_API_TARGETS_RETRIEVE_URL


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


@patch("probely_cli.sdk.client.ProbelyAPIClient.get")
def test_retrieve_target__success_api_call(api_client_mock: Mock):
    resp_code = 200
    testable_id = "2DZkoZH8WMEM"
    resp_content = {"id": testable_id}

    api_client_mock.return_value = (resp_code, resp_content)

    retrieve_target(testable_id)

    expected_call_url = PROBELY_API_TARGETS_RETRIEVE_URL.format(id=testable_id)
    api_client_mock.assert_called_with(expected_call_url)


@patch("probely_cli.sdk.client.ProbelyAPIClient.get")
def test_retrieve_target__unsuccessful_api_call(api_client_mock: Mock):
    not_found_id = "random_target_id"
    api_client_mock.return_value = (404, {})

    with pytest.raises(BaseException) as exc_info:
        retrieve_target(not_found_id)

    raised_exception = exc_info.value
    assert isinstance(raised_exception, ProbelyObjectNotFound)
    assert raised_exception.not_found_object_id == not_found_id

    api_client_mock.reset_mock()

    expected_error = {"detail": "Specific error stuff"}
    api_client_mock.return_value = (400, expected_error)

    with pytest.raises(BaseException) as exc_info:
        retrieve_target(not_found_id)

    raised_exception = exc_info.value
    assert isinstance(raised_exception, ProbelyRequestFailed)
    assert raised_exception.reason == expected_error


@patch("probely_cli.sdk.client.ProbelyAPIClient.get")
def test_retrieve_targets__success_api_calls(api_client_mock: Mock):
    ids_list = ["id1", "id2"]
    api_client_mock.side_effect = [
        (200, {"id": ids_list[0]}),
        (200, {"id": ids_list[1]}),
    ]
    results = retrieve_targets(ids_list)

    assert api_client_mock.call_count == len(
        ids_list
    ), "Expected one API for each target ID"
    assert isinstance(results, list), "Expected a list of results"

    results_ids = set([r["id"] for r in results])
    assert results_ids == set(ids_list), "Expected one result for each target ID"
