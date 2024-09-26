import importlib
import json
from unittest.mock import MagicMock, Mock, patch
from urllib.parse import urlencode

import pytest
import requests
from requests import PreparedRequest

from probely_cli import retrieve_target, settings
from probely_cli.exceptions import ProbelyApiUnavailable, ProbelyMissConfig
from probely_cli.sdk.client import Probely, ProbelyAPIClient
from tests.conftest import probely_cli


@pytest.fixture
def api_calls_without_session_cache():
    # Session are kept for multiple request runs.
    # To have multiple tests cases on sessions status it must be reset.
    ProbelyAPIClient.flush_session_cache()


@pytest.fixture
def set_default_api_key():
    with patch("probely_cli.sdk.client.settings.PROBELY_API_KEY", "random_key"):
        yield


def test_probely_api_client__session_auth_api_key_from_settings(
    api_calls_without_session_cache,
):
    env_var_api_key: str = "test_probely_api_key"

    with patch(
        "probely_cli.sdk.client.settings.PROBELY_API_KEY",
        new=env_var_api_key,
    ):
        session = ProbelyAPIClient._build_session()

    assert isinstance(session, requests.Session)
    assert (
        "Authorization" in session.headers
    ), "Expected default configuration to exists"

    assert (
        "JWT " + env_var_api_key in session.headers["Authorization"]
    ), "Expected default api_key from envvars"


def test_probely_api_client__session_auth_api_key_from_args(
    api_calls_without_session_cache,
):
    args_api_key = "local_var_api_key"

    Probely.init(api_key=args_api_key)  # simulation of command with --api_key arg

    session = ProbelyAPIClient._build_session()

    assert isinstance(session, requests.Session)
    assert (
        "Authorization" in session.headers
    ), "Expected default configuration to exists"

    assert (
        "JWT " + args_api_key in session.headers["Authorization"]
    ), "Expected default api_key from args"


def test_probely_api_client__session_auth_api_key_args_overwrites_settings(
    api_calls_without_session_cache,
):
    args_api_key = "local_var_api_key"
    Probely.init(api_key=args_api_key)  # simulation of command with --api_key arg

    env_var_api_key: str = "test_probely_api_key"
    with patch("probely_cli.sdk.client.settings.PROBELY_API_KEY", env_var_api_key):
        session = ProbelyAPIClient._build_session()

    assert (
        "JWT " + args_api_key in session.headers["Authorization"]
    ), "Expected default api_key from args"


def test_probely_api_client__session_is_being_cached(api_calls_without_session_cache):
    session_first_run = ProbelyAPIClient._build_session()
    session_second_run = ProbelyAPIClient._build_session()

    assert id(session_first_run) == id(session_second_run)


@patch("probely_cli.sdk.client.requests.Session.send")
def test_probely_api_client__cli_user_agent_is_added(
    requests_session_send_mock: MagicMock,
    api_calls_without_session_cache,
    probely_cli,
):
    requests_session_send_mock.return_value = Mock(status_code=200, content="{}")

    assert (
        ProbelyAPIClient._session_cache is None
    ), "Test setup fail. Expected no session cache from other tests"

    Probely.reset_config()
    assert Probely._instance is None, "Test setup fail. Expected no config instance"

    settings.IS_CLI = True
    settings.PROBELY_API_KEY = "test_api_key"

    ProbelyAPIClient.get("https://www.test.com")

    assert requests_session_send_mock.call_count == 1

    call_args, _call_kwargs = requests_session_send_mock.call_args
    prepared_request_used = call_args[0]
    assert "User-Agent" in prepared_request_used.headers
    assert "ProbelyCLI" in prepared_request_used.headers["User-Agent"]

    # clean up stuff that can affect other tests
    Probely.reset_config()
    importlib.reload(settings)


@patch("probely_cli.sdk.client.requests.Session.send")
def test_probely_api_client__sdk_user_agent_is_added(
    requests_session_send_mock: MagicMock,
    api_calls_without_session_cache,
    probely_cli,
):
    requests_session_send_mock.return_value = Mock(status_code=200, content="{}")

    assert (
        ProbelyAPIClient._session_cache is None
    ), "Test setup fail. Expected no session cache from other tests"

    Probely.reset_config()
    assert Probely._instance is None, "Test setup fail. Expected no config instance"

    importlib.reload(settings)
    settings.PROBELY_API_KEY = None

    assert settings.IS_CLI is False, "Test setup fail. Expected default config"
    assert settings.PROBELY_API_KEY is None, "Test setup fail. Expected default config"

    Probely.init(api_key="init_api_key")
    retrieve_target("random_id")

    assert requests_session_send_mock.call_count == 1
    call_args, _call_kwargs = requests_session_send_mock.call_args
    prepared_request_used = call_args[0]
    assert "User-Agent" in prepared_request_used.headers
    assert "ProbelySDK" in prepared_request_used.headers["User-Agent"]

    assert settings.IS_CLI == False, "Expect setting to reflect user agent context"

    # clean up stuff that can affect other tests
    Probely.reset_config()
    importlib.reload(settings)


@patch("probely_cli.sdk.client.requests.Session.send")
def test_probely_api_client__correct_content_and_url_are_request(
    requests_session_send_mock: Mock,
    set_default_api_key,
):

    random_url = "https://randomurl.com/"
    random_content = {"key1": "value1", "key2": "value2"}
    testable_content = json.dumps(random_content)

    requests_session_send_mock.return_value = Mock(
        status_code=200,
        content=testable_content,
    )

    ProbelyAPIClient.post(url=random_url, payload=random_content)

    args = requests_session_send_mock.call_args.args[0]

    assert isinstance(args, PreparedRequest)

    assert args.body == str.encode(testable_content)
    assert args.path_url == "/"
    assert args.url == random_url


@patch("probely_cli.sdk.client.requests.Session.send")
def test_probely_api_client__url_is_populated_with_query_params(
    requests_session_send_mock: Mock,
    set_default_api_key,
):
    random_url = "https://randomurl.com/"
    query_params = {"key1": "value1", "key2": "value2"}
    expected_url_query_params = urlencode(query_params)

    requests_session_send_mock.return_value = Mock(
        status_code=200,
        content='{"not": "relevant"}',
    )

    ProbelyAPIClient.get(url=random_url, query_params=query_params)

    args = requests_session_send_mock.call_args.args[0]

    assert isinstance(args, PreparedRequest)

    assert args.path_url == "/?" + expected_url_query_params
    assert args.url == random_url + "?" + expected_url_query_params


@patch("probely_cli.sdk.client.requests.Session.send")
def test_probely_api_client__content_when_content_invalid(
    requests_session_send_mock: Mock,
    set_default_api_key,
):
    requests_session_send_mock.return_value = Mock(
        content="invalid json string",
    )

    with pytest.raises(ProbelyApiUnavailable) as raised_ex:
        ProbelyAPIClient.get("https://irrelevant_url.com")

    assert str(raised_ex.value) == "API is unavailable. Contact support."


@patch("probely_cli.sdk.client.requests.Session.send")
def test_probely_api_client__return_is_correct(
    requests_session_send_mock: Mock,
    set_default_api_key,
):
    expected_status_code = 200
    expected_content = {"key1": "value1", "key2": "value2"}
    testable_content = json.dumps(expected_content)

    requests_session_send_mock.return_value = Mock(
        status_code=200,
        content=testable_content,
    )

    returned_status_code, returned_content = ProbelyAPIClient.get("https://url.com")

    assert returned_status_code == expected_status_code
    assert isinstance(returned_content, dict)
    assert returned_content == expected_content


@patch("probely_cli.sdk.client.requests.Session.send")
def test_probely_api_client__filters_added_as_query_params(
    requests_session_send_mock: Mock,
    set_default_api_key,
):
    requests_session_send_mock.return_value = Mock(
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

    ProbelyAPIClient.get("https://url.com", query_params=query_params)

    requests_session_send_mock.assert_called_once()

    prepared_request_used = requests_session_send_mock.call_args[0][0]
    expected_url_called = "https://url.com/?k1=v1&k2=v2&f1=s1&f_l1=e1&f_l1=e2&f_l2=e3"

    assert prepared_request_used.url == expected_url_called


def test_probely_instance__cant_be_instantiated():
    with pytest.raises(BaseException) as exc_info:
        Probely()

    exc = exc_info.value
    assert isinstance(exc, NotImplementedError)
    assert str(exc) == "Use Probely.init() to configure"


@patch("probely_cli.sdk.client.settings.PROBELY_API_KEY", None)
def test_probely_instance__no_api_key():
    Probely.reset_config()
    assert Probely._instance is None, "Test setup fail. Expected no config instance"

    with pytest.raises(BaseException) as exc_info:
        Probely.init()

    exc = exc_info.value
    assert isinstance(exc, ProbelyMissConfig)
    assert str(exc) == "Missing API_KEY config"

    Probely.reset_config()


def test_probely_instance__config_from_settings():
    Probely.reset_config()
    assert Probely._instance is None, "Test setup fail. Expected no config instance"

    api_key_from_settings = "api_key_from_settings"

    with patch(
        "probely_cli.sdk.client.settings.PROBELY_API_KEY", api_key_from_settings
    ):
        Probely.init()

    assert Probely.get_config()["api_key"] == api_key_from_settings

    Probely.reset_config()


def test_probely_instance__config_from_instantiation():
    Probely.reset_config()
    assert Probely._instance is None, "Test setup fail. Expected no config instance"

    api_key_from_settings = "api_key_from_settings"
    api_key_from_instantiation = "api_key_from_instantiation"

    with patch(
        "probely_cli.sdk.client.settings.PROBELY_API_KEY", api_key_from_settings
    ):
        Probely.init(api_key=api_key_from_instantiation)

    current_probely_config = Probely.get_config()
    assert (
        current_probely_config["api_key"] != api_key_from_settings
    ), "Expected settings values to be overridden"
    assert current_probely_config["api_key"] == api_key_from_instantiation

    Probely.reset_config()


def test_probely_instance__reconfig_exiting_config():
    Probely.reset_config()
    assert Probely._instance is None, "Test setup fail. Expected no config instance"

    api_key_from_settings = "api_key_from_settings"
    api_key_from_init = "api_key_from_init"

    with patch(
        "probely_cli.sdk.client.settings.PROBELY_API_KEY", api_key_from_settings
    ):
        current_probely_config: dict = Probely.get_config()
        assert (
            current_probely_config["api_key"] == api_key_from_settings
        ), "get_config() should retrieve default values"

        Probely.init(api_key=api_key_from_init)
        current_probely_config: dict = Probely.get_config()
        assert (
            current_probely_config["api_key"] == api_key_from_init
        ), "Probely.init() should override existing config"
