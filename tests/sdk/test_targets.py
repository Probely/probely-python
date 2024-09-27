from copy import deepcopy
from unittest.mock import MagicMock, Mock, patch

import pytest

from probely_cli.exceptions import (
    ProbelyBadRequest,
    ProbelyObjectNotFound,
    ProbelyRequestFailed,
)
from probely_cli.sdk.enums import TargetAPISchemaTypeEnum, TargetTypeEnum
from probely_cli.sdk.targets import (
    add_target,
    delete_target,
    delete_targets,
    list_targets,
    retrieve_target,
    retrieve_targets,
    update_target,
    update_targets,
)
from probely_cli.settings import (
    PROBELY_API_TARGETS_BULK_DELETE_URL,
    PROBELY_API_TARGETS_BULK_UPDATE_URL,
    PROBELY_API_TARGETS_DELETE_URL,
    PROBELY_API_TARGETS_RETRIEVE_URL,
)
from tests.testable_api_responses import RETRIEVE_TARGET_200_RESPONSE


@patch("probely_cli.sdk.client.ProbelyAPIClient.get")
def test_list_targets__ok(api_client_mock: Mock):
    expected_content = [{"list": "of objects1"}, {"list": "of objects2"}]
    response_content = {"results": expected_content, "page_total": 1}

    api_client_mock.return_value = (200, response_content)

    r = list(list_targets())
    assert r == expected_content


@patch("probely_cli.sdk.client.ProbelyAPIClient.get")
def test_list_targets__unsuccessful(api_client_mock: Mock):
    invalid_status_code = 400
    error_message = "request invalid"
    error_response_content = {"detail": error_message}

    api_client_mock.return_value = (invalid_status_code, error_response_content)

    with pytest.raises(ProbelyRequestFailed) as exc:
        list(list_targets())

        raised_exception = exc.value
        assert str(raised_exception) == error_message


@patch("probely_cli.sdk.client.ProbelyAPIClient.get")
def test_list_targets__filters(api_client_mock: Mock):
    resp_code = 200
    resp_content = {"results": "random content", "page_total": 1}

    api_client_mock.return_value = (resp_code, resp_content)

    expected_filter_key = "filter1"
    filters = {expected_filter_key: "value1"}
    list(list_targets(targets_filters=filters))

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


@patch("probely_cli.sdk.client.ProbelyAPIClient.delete")
def test_delete_target__success_api_call(api_client_mock: Mock):
    resp_code = 204
    testable_id = "2DZkoZH8WMEM"
    resp_content = {"id": testable_id}

    api_client_mock.return_value = (resp_code, resp_content)

    delete_target(testable_id)

    expected_call_url = PROBELY_API_TARGETS_DELETE_URL.format(id=testable_id)

    api_client_mock.assert_called_with(url=expected_call_url)


@patch("probely_cli.sdk.client.ProbelyAPIClient.delete")
def test_delete_target__unsuccessful_api_call(api_client_mock: Mock):
    resp_code = 400
    testable_id = "2DZkoZH8WMEM"

    api_client_mock.return_value = (resp_code, {})
    with pytest.raises(BaseException) as exc_info:
        delete_target([testable_id])

    raised_exception = exc_info.value
    assert isinstance(raised_exception, ProbelyRequestFailed)

    api_client_mock.reset_mock()

    not_found_id = "random_target_id"
    api_client_mock.return_value = (404, {})

    with pytest.raises(BaseException) as exc_info:
        delete_target(not_found_id)

    raised_exception = exc_info.value
    assert isinstance(raised_exception, ProbelyObjectNotFound)
    assert raised_exception.not_found_object_id == not_found_id


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
def test_delete_targets__unsuccessful_api_call(api_client_mock: Mock):
    resp_code = 400
    testable_id = "2DZkoZH8WMEM"

    api_client_mock.return_value = (resp_code, {})
    with pytest.raises(BaseException) as exc_info:
        delete_targets([testable_id])

    expected_call_url = PROBELY_API_TARGETS_BULK_DELETE_URL
    api_client_mock.assert_called_with(
        url=expected_call_url, payload={"ids": [testable_id]}
    )
    raised_exception = exc_info.value
    assert isinstance(raised_exception, ProbelyRequestFailed)


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


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
def test_add_target__success_api_call(
    api_client_mock: MagicMock,
    valid_add_targets_api_response,
):
    expected_content = valid_add_targets_api_response
    response_content = valid_add_targets_api_response

    api_client_mock.return_value = (201, response_content)

    r = add_target("https://www.example.com")
    assert r == expected_content, "Expected object output from API"


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
def test_add_target__unsuccessful_api_call(
    api_client_mock: MagicMock,
):
    invalid_status_code = (401,)
    error_message = ("request invalid",)
    error_response_content = {"detail": error_message}

    api_client_mock.return_value = (invalid_status_code, error_response_content)

    with pytest.raises(ProbelyRequestFailed) as exc:
        add_target("https://www.example.com")

        raised_exception = exc.value
        assert str(raised_exception) == error_message


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
def test_add_target__api_call_with_default_query_params(
    api_client_mock: MagicMock,
):
    base_query_params = {
        "duplicate_check": False,
        "skip_reachability_check": True,
    }

    with pytest.raises(BaseException) as _:
        add_target("https://www.example.com")

    assert api_client_mock.call_count == 1, "Expected call"
    _, kwargs = api_client_mock.call_args
    assert kwargs["query_params"] == base_query_params


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
def test_add_target__api_call_with_payload(
    api_client_mock: MagicMock,
):
    expected_url = "https://www.example.com"

    valid_file_input = {
        "type": "single",
        "site": {
            "name": "testable_target_name_from_file",
            "url": "https://testable_url_from_file.com",
            "api_scan_settings": {
                "api_schema_type": "postman",
                "api_schema_url": "https://target_from_file.com/api_schema.json",
            },
        },
        "other_api_property": "control_value",
    }

    expected_payload = deepcopy(valid_file_input)
    expected_payload["site"]["url"] = expected_url

    with pytest.raises(BaseException) as _:  # not testing the api output
        add_target(expected_url, extra_payload=valid_file_input)

    assert api_client_mock.call_count == 1, "Expected call"

    _, kwargs = api_client_mock.call_args
    assert kwargs["payload"] == expected_payload, "Expected payload to be sent"
    assert id(kwargs["payload"]) != id(
        expected_payload
    ), "Watch out for ids of test data"


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
def test_add_target__arguments_are_api_call_arguments(
    api_client_mock: MagicMock,
):
    target_url = "https://www.name_overwrite.com"
    target_name = "name_overwrite"
    target_type = TargetTypeEnum.API
    api_schema_file_url = "https://api_schema_file_url_overwrite.com/sh.yaml"
    api_schema_type = TargetAPISchemaTypeEnum.OPENAPI

    other_api_properties = {"random_api_property": "random_value"}

    with pytest.raises(BaseException) as _:  # not testing the api output
        add_target(
            target_url,
            target_name=target_name,
            target_type=target_type,
            api_schema_file_url=api_schema_file_url,
            api_schema_type=api_schema_type,
            extra_payload=other_api_properties,
        )

    expected_payload = {
        "type": target_type.api_request_value,
        "site": {
            "name": target_name,
            "url": target_url,
            "api_scan_settings": {
                "api_schema_type": api_schema_type.api_request_value,
                "api_schema_url": api_schema_file_url,
            },
        },
        **other_api_properties,
    }

    assert api_client_mock.call_count == 1, "Expected call"
    _, kwargs = api_client_mock.call_args

    assert (
        kwargs["payload"] == expected_payload
    ), "Expected arguments to be sent as pyload"


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
def test_add_target__api_call_with_payload_overrides(
    api_client_mock: MagicMock,
):
    valid_file_input = {
        "type": "single",
        "site": {
            "name": "testable_target_name_from_file",
            "url": "https://testable_url_from_file.com",
            "api_scan_settings": {
                "api_schema_type": "postman",
                "api_schema_url": "https://target_from_file.com/api_schema.json",
            },
        },
        "other_api_property": "control_value",
    }

    target_url_overwrite = "https://www.name_overwrite.com"
    target_name_overwrite = "name_overwrite"
    target_type_overwrite = TargetTypeEnum.API
    api_schema_type_overwrite = TargetAPISchemaTypeEnum.OPENAPI
    api_schema_file_url_overwrite = "https://api_schema_file_url_overwrite.com/sh.yaml"

    expected_payload = deepcopy(valid_file_input)
    expected_payload["type"] = target_type_overwrite.api_request_value
    expected_payload["site"]["name"] = target_name_overwrite
    expected_payload["site"]["url"] = target_url_overwrite
    expected_payload["site"]["api_scan_settings"][
        "api_schema_type"
    ] = api_schema_type_overwrite.api_request_value
    expected_payload["site"]["api_scan_settings"][
        "api_schema_url"
    ] = api_schema_file_url_overwrite

    with pytest.raises(BaseException) as _:  # not testing the api output
        add_target(
            target_url_overwrite,
            target_name=target_name_overwrite,
            target_type=target_type_overwrite,
            api_schema_file_url=api_schema_file_url_overwrite,
            api_schema_type=api_schema_type_overwrite,
            extra_payload=valid_file_input,
        )

    assert api_client_mock.call_count == 1, "Expected call"
    _, kwargs = api_client_mock.call_args

    assert kwargs["payload"] == expected_payload, "Expected overrides to take effect"
    assert id(kwargs["payload"]) != id(
        expected_payload
    ), "Watch out for ids of test data"


@patch("probely_cli.sdk.targets.ProbelyAPIClient.patch")
def test_update_target__successful_api_call(api_client_mock: Mock):
    target_id = "sample_target_id"
    payload = {"description": "Updated description"}

    expected_response_content = RETRIEVE_TARGET_200_RESPONSE.copy()
    expected_response_content["id"] = target_id
    expected_response_content["site"]["description"] = payload["description"]

    api_client_mock.return_value = (200, expected_response_content)
    expected_endpoint_url = PROBELY_API_TARGETS_RETRIEVE_URL.format(id=target_id)

    result = update_target(target_id, payload)

    assert result == expected_response_content
    api_client_mock.assert_called_with(expected_endpoint_url, payload=payload)


@patch("probely_cli.sdk.client.ProbelyAPIClient.patch")
def test_update_target__unsuccessful_api_call(api_client_mock: Mock):
    target_id = "sample_target_id"
    payload = {"type": "apiX"}

    # Ensure ProbelyBadRequest is raised if API returns status code 400
    api_validation_error = {"type": "Invalid type value"}
    api_client_mock.return_value = (400, api_validation_error)

    with pytest.raises(ProbelyBadRequest) as exc_info:
        update_target(target_id, payload)
        assert exc_info.value.response_payload == api_validation_error

    # Ensure ProbelyObjectNotFound is raised if API returns status code 404
    api_client_mock.return_value = (404, {})
    with pytest.raises(ProbelyObjectNotFound) as exc_info:
        update_target(target_id, payload)
        assert exc_info.value.not_found_object_id == target_id

    # Ensure ProbelyRequestFailed is raised if API returns some another notok status code
    api_error = {"detail": "No entitlement to update this target"}
    api_client_mock.return_value = (403, api_error)
    with pytest.raises(ProbelyRequestFailed) as exc_info:
        update_target(target_id, payload)
        assert exc_info.value.reason == api_error


@patch("probely_cli.sdk.targets.ProbelyAPIClient.post")
@patch("probely_cli.sdk.targets.validate_resource_ids")
@patch("probely_cli.sdk.targets.retrieve_targets")
def test_update_targets__successful_api_call(
    retrieve_targets_mock: Mock,
    validate_resource_ids_mock: Mock,
    api_client_mock: Mock,
):
    validate_resource_ids_mock.return_value = None  # target IDs are valid

    target_ids = ["target_id1", "target_id2"]
    payload = {"name": "test name", "description": "test description"}

    expected_payload_on_api_call = {"ids": target_ids, **payload}
    api_client_mock.return_value = (200, {"ids": target_ids})

    expected_target_bodies = [
        {"id": "target_id1", "name": "test name", "description": "test description"},
        {"id": "target_id2", "name": "test name", "description": "test description"},
    ]
    retrieve_targets_mock.return_value = expected_target_bodies

    result = update_targets(target_ids, payload)

    api_client_mock.assert_called_with(
        PROBELY_API_TARGETS_BULK_UPDATE_URL, payload=expected_payload_on_api_call
    )

    # Ensure that Targets are retrieved after update, to get the updated data
    retrieve_targets_mock.assert_called_once_with(target_ids)

    assert result == expected_target_bodies


@patch("probely_cli.sdk.client.ProbelyAPIClient.post")
@patch("probely_cli.sdk.targets.validate_resource_ids")
def test_update_targets__unsuccessful_api_call(
    validate_resource_ids_mock: Mock,
    api_client_mock: Mock,
):
    payload = {"key": "value", "name": "new_name"}

    # Ensure ProbelyObjectNotFound is raised if invalid target IDs are provided:
    target_ids = ["invalid_id1"]

    validate_resource_ids_mock.side_effect = ProbelyObjectNotFound(id=target_ids[0])
    with pytest.raises(ProbelyObjectNotFound) as exc_info:
        update_targets(target_ids, payload)
        assert exc_info.value.not_found_object_id == target_ids[0]

    # Ensure ProbelyBadRequest is raised if API returns status code 400
    validate_resource_ids_mock.side_effect = None
    validate_resource_ids_mock.returne_value = (
        None  # Target IDs are valid for this scenario
    )

    target_ids = ["target_id1", "target_id2"]
    api_validation_error = {"type": "Invalid type value"}
    api_client_mock.return_value = (400, api_validation_error)

    with pytest.raises(ProbelyBadRequest) as exc_info:
        update_targets(target_ids, payload)
        assert exc_info.value.response_payload == api_validation_error

    # Ensure ProbelyRequestFailed is raised if API returns some another notok status code
    api_error = {"detail": "Authentication credentials were not provided."}
    api_client_mock.return_value = (401, api_error)
    with pytest.raises(ProbelyRequestFailed) as exc_info:
        update_targets(payload, payload)
        assert exc_info.value.reason == api_error
