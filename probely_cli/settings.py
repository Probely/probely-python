import os
import configparser


PROBELY_CONFIG_FILE_PATH = os.path.expanduser("~") + "/.probely/config"

CONFIG_PARSER = configparser.ConfigParser()
CONFIG_PARSER.read(PROBELY_CONFIG_FILE_PATH)


def _get_probely_api_key():
    env_var_api_key = os.getenv("PROBELY_API_TOKEN", None)

    if env_var_api_key:
        return env_var_api_key

    config_file_exists = os.path.isfile(PROBELY_CONFIG_FILE_PATH)
    if config_file_exists:

        try:
            return CONFIG_PARSER["AUTH"]["api_key"]
        except KeyError:
            pass

    return None


PROBELY_API_KEY = _get_probely_api_key()

PROBELY_API_URL_BASE = os.getenv(
    "PROBELY_API_URL_BASE", default="https://api.qa.eu.probely.com/"
)

# URLs
PROBELY_API_TARGETS_URL = PROBELY_API_URL_BASE + "targets/"
