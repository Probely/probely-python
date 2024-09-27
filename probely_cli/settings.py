import configparser
import os
from pathlib import Path
from typing import Union

import marshmallow
from environs import Env

PROBELY_CONFIG_DIR = ".probely"
PROBELY_CONFIG_DIR_PATH = Path.home() / PROBELY_CONFIG_DIR
PROBELY_CONFIG_FILE = "config"
PROBELY_CONFIG_FILE_PATH = PROBELY_CONFIG_DIR_PATH / PROBELY_CONFIG_FILE

CONFIG_PARSER = configparser.ConfigParser()
CONFIG_PARSER.read(PROBELY_CONFIG_FILE_PATH)


TRUTHY_VALUES = ["TRUE"]
FALSY_VALUES = ["FALSE"]

IS_CLI = False

env = Env()


def _get_probely_api_key():
    env_var_api_key = env.str("PROBELY_API_KEY", None)

    if env_var_api_key:
        return env_var_api_key

    config_file_exists = os.path.isfile(PROBELY_CONFIG_FILE_PATH)
    if config_file_exists:

        try:
            return CONFIG_PARSER["AUTH"]["api_key"]
        except KeyError:
            pass

    return None


def _get_probely_debug():
    env_var_probely_debug = env.bool("PROBELY_DEBUG", None)
    if env_var_probely_debug is not None:
        return env_var_probely_debug

    config_file_exists = os.path.isfile(PROBELY_CONFIG_FILE_PATH)
    if config_file_exists:
        try:
            debug_config = CONFIG_PARSER["SETTINGS"]["debug"]
            bool_field = marshmallow.fields.Boolean()
            return bool_field.deserialize(debug_config)
        except (KeyError, marshmallow.ValidationError):
            # TODO: add feedback when validationError
            pass

    return False


# TODO: first attempt of general implementation. Never used, needs testing
def _get_config(
    env_var: str,
    config_file_setting_path: list,
    default_value: Union[str, bool, None] = None,
) -> Union[str, bool, None]:
    env_var_value = os.getenv(env_var, None)
    if env_var_value:
        return env_var_value

    config_file_exists = os.path.isfile(PROBELY_CONFIG_FILE_PATH)
    if config_file_exists:
        try:
            current_parser_or_value = CONFIG_PARSER
            # TODO Test
            # for step in config_file_setting_path:
            #     current_parser_or_value = current_parser[step]

            return current_parser_or_value
        except KeyError:
            pass

    return default_value


PROBELY_API_KEY = _get_probely_api_key()
IS_DEBUG_MODE = _get_probely_debug()

CLI_ACCEPTED_FILE_EXTENSIONS = [".yaml", ".yml"]


def get_probely_api_base_url():
    probely_api_url: str = os.getenv(
        "PROBELY_API_BASE_URL",
        default="https://api.probely.com/",
    )

    if probely_api_url and probely_api_url[-1] != "/":
        probely_api_url = f"{probely_api_url}/"

    return probely_api_url


PROBELY_API_BASE_URL = get_probely_api_base_url()

PROBELY_API_TARGETS_URL = PROBELY_API_BASE_URL + "targets/"
PROBELY_API_TARGETS_RETRIEVE_URL = PROBELY_API_TARGETS_URL + "{id}/"
PROBELY_API_TARGETS_DELETE_URL = PROBELY_API_TARGETS_URL + "{id}/"
PROBELY_API_TARGETS_BULK_DELETE_URL = PROBELY_API_TARGETS_URL + "bulk/delete/"
PROBELY_API_TARGETS_BULK_UPDATE_URL = PROBELY_API_TARGETS_URL + "bulk/update/"
PROBELY_API_TARGETS_START_SCAN_URL = PROBELY_API_TARGETS_URL + "{target_id}/scan_now/"

PROBELY_API_SCANS_URL = PROBELY_API_BASE_URL + "scans/"
PROBELY_API_SCANS_BULK_CANCEL_URL = PROBELY_API_SCANS_URL + "bulk/cancel/"
PROBELY_API_SCANS_BULK_RESUME_URL = PROBELY_API_SCANS_URL + "bulk/resume/"
PROBELY_API_SCANS_BULK_PAUSE_URL = PROBELY_API_SCANS_URL + "bulk/pause/"
PROBELY_API_SCANS_BULK_START_URL = PROBELY_API_SCANS_URL + "bulk/start/"
PROBELY_API_SCAN_PAUSE_URL = (
    PROBELY_API_TARGETS_URL + "{target_id}/scans/{scan_id}/pause/"
)
PROBELY_API_SCAN_CANCEL_URL = (
    PROBELY_API_TARGETS_URL + "{target_id}/scans/{scan_id}/cancel/"
)
PROBELY_API_SCAN_RESUME_URL = (
    PROBELY_API_TARGETS_URL + "{target_id}/scans/{scan_id}/resume/"
)

PROBELY_API_FINDINGS_URL = PROBELY_API_BASE_URL + "findings/"
PROBELY_API_FINDINGS_RETRIEVE_URL = PROBELY_API_FINDINGS_URL + "{id}/"

PROBELY_API_PAGE_SIZE = 50
