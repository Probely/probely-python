import importlib
from unittest.mock import patch, MagicMock

from probely_cli import Probely, settings


@patch("probely_cli.sdk.client.requests.Session.send")
def test_probely_cli__is_cli_setting(
    _requests_session_send_mock: MagicMock,
    probely_cli,
):
    importlib.reload(settings)
    assert settings.IS_CLI == False, "Test setup fail. Expected default value"

    # random CLI command
    probely_cli("targets get", return_list=True)

    assert settings.IS_CLI == True, "Expect settings to reflect running context"

    # clean up stuff that can affect other tests
    Probely.reset_config()
    importlib.reload(settings)


@patch("probely_cli.sdk.client.requests.Session.send")
def test_probely_cli__api_key_argument_overrides_config(
    _requests_session_send_mock: MagicMock,
    probely_cli,
):
    api_key_from_settings = "api_key_from_settings"
    api_key_from_args = "api_key_from_args"

    with patch(
        "probely_cli.sdk.client.settings.PROBELY_API_KEY", api_key_from_settings
    ):
        Probely.init()
        assert Probely.get_config()["api_key"] == api_key_from_settings

        Probely.reset_config()
        # random command to test CLI --api-key arg
        probely_cli("targets get --api-key", api_key_from_args, return_list=True)

        assert (
            Probely.get_config()["api_key"] == api_key_from_args
        ), "Expected api_key argument to override settings"

    # clean up stuff that can affect other tests
    Probely.reset_config()
