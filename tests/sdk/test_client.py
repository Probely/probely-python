from unittest import mock

import requests

from probely_cli.sdk.client import _get_client, Probely


# TODO: Add test for priority of env vars vs config file
def test_client_auth():
    env_var_api_key: str = "test_probely_api_key"

    with mock.patch(
        "probely_cli.sdk.client.settings.PROBELY_API_KEY",
        new=env_var_api_key,
    ):
        session = _get_client()

    assert isinstance(session, requests.Session)
    assert (
        "Authorization" in session.headers
    ), "Expected default configuration to exists"

    assert (
        "JWT " + env_var_api_key in session.headers["Authorization"]
    ), "Expected default api_key from envvars"

    local_api_key = "local_var_api_key"
    Probely.init(api_key=local_api_key)
    session = _get_client()

    assert (
        "JWT " + local_api_key in session.headers["Authorization"]
    ), "Expected local api_key to be in effect"
