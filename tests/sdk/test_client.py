import json
from unittest import mock
from unittest.mock import patch, Mock
from urllib.parse import urlencode

import pytest
import requests
from requests import Response, PreparedRequest

from probely_cli.exceptions import ProbelyApiUnavailable
from probely_cli.sdk.client import Probely, ProbelyAPIClient


# TODO: Add test for priority of env vars vs config file
def test_probely_api_client__session_auth_content():
    env_var_api_key: str = "test_probely_api_key"

    with mock.patch(
        "probely_cli.sdk.client.settings.PROBELY_API_KEY",
        new=env_var_api_key,
    ):
        session = ProbelyAPIClient()._build_session()

    assert isinstance(session, requests.Session)
    assert (
        "Authorization" in session.headers
    ), "Expected default configuration to exists"

    assert (
        "JWT " + env_var_api_key in session.headers["Authorization"]
    ), "Expected default api_key from envvars"

    local_api_key = "local_var_api_key"

    Probely.init(api_key=local_api_key)  # simulation of command with --api_key arg

    session = ProbelyAPIClient()._build_session()

    assert (
        "JWT " + local_api_key in session.headers["Authorization"]
    ), "Expected local api_key to be in effect"


@patch("probely_cli.sdk.client.requests.Session.send")
def test_probely_api_client__correct_content_and_url_are_request(
    session_send_mock: Mock,
):
    random_url = "https://randomurl.com/"
    random_content = {"key1": "value1", "key2": "value2"}
    testable_content = json.dumps(random_content)

    session_send_mock.return_value = Mock(
        status_code=200,
        content=testable_content,
    )

    ProbelyAPIClient().post(url=random_url, payload=random_content)

    args = session_send_mock.call_args.args[0]

    assert isinstance(args, PreparedRequest)

    assert args.body == str.encode(testable_content)
    assert args.path_url == "/"
    assert args.url == random_url


@patch("probely_cli.sdk.client.requests.Session.send")
def test_probely_api_client__url_is_populated_with_query_params(
    session_send_mock: Mock,
):
    random_url = "https://randomurl.com/"
    query_params = {"key1": "value1", "key2": "value2"}
    expected_url_query_params = urlencode(query_params)

    session_send_mock.return_value = Mock(
        status_code=200,
        content='{"not": "relevant"}',
    )

    ProbelyAPIClient().get(url=random_url, query_params=query_params)

    args = session_send_mock.call_args.args[0]

    assert isinstance(args, PreparedRequest)

    assert args.path_url == "/?" + expected_url_query_params
    assert args.url == random_url + "?" + expected_url_query_params


@patch("probely_cli.sdk.client.requests.Session.send")
def test_probely_api_client__content_when_content_invalid(session_send_mock: Mock):
    session_send_mock.return_value = Mock(
        content="invalid json string",
    )

    with pytest.raises(ProbelyApiUnavailable) as raised_ex:
        ProbelyAPIClient().get("https://irrelevant_url.com")

    assert str(raised_ex.value) == "API is unavailable. Contact support."


@patch("probely_cli.sdk.client.requests.Session.send")
def test_probely_api_client__return_is_correct(session_send_mock: Mock):
    expected_status_code = 200
    expected_content = {"key1": "value1", "key2": "value2"}
    testable_content = json.dumps(expected_content)

    session_send_mock.return_value = Mock(
        status_code=200,
        content=testable_content,
    )

    returned_status_code, returned_content = ProbelyAPIClient().get("https://url.com")

    assert returned_status_code == expected_status_code
    assert isinstance(returned_content, dict)
    assert returned_content == expected_content


@patch("probely_cli.sdk.client.requests.Session.send")
def test_probely_api_client__filters_added_as_query_params(session_send_mock: Mock):
    session_send_mock.return_value = Mock(
        status_code=200,
        content="{}",
    )

    query_params = {
        "k1": "v1",
        "k2": "v2",
    }
    filters = {
        "f1": "s1",
        "f_l1": [
            "e1",
            "e2",
        ],
        "f_l2": [
            "e3",
        ],
    }

    query_params.update(filters)

    ProbelyAPIClient().get("https://url.com", query_params=query_params)

    session_send_mock.assert_called_once()

    prepared_request_used = session_send_mock.call_args[0][0]
    expected_url_called = "https://url.com/?k1=v1&k2=v2&f1=s1&f_l1=e1&f_l1=e2&f_l2=e3"
    assert prepared_request_used.url == expected_url_called
