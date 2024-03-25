import os
import configparser

PROBELY_CONFIG_DIR_PATH = os.path.expanduser("~") + "/.probely/"
PROBELY_CONFIG_FILE_PATH = PROBELY_CONFIG_DIR_PATH + "config"

CONFIG_PARSER = configparser.ConfigParser()
CONFIG_PARSER.read(PROBELY_CONFIG_FILE_PATH)


def _get_probely_api_key():
    env_var_api_key = os.getenv("PROBELY_API_KEY", None)

    print("yes, this is api key:", env_var_api_key)
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


# from dynaconf import Dynaconf
#
# app_settings = Dynaconf(
#     envvar_prefix="PROBELY",
#     root_path=PROBELY_CONFIG_DIR_PATH,
#     settings_files=["config.toml"],
#     load_dotenv=True,
# )
#
# print("these are the app settings")
# print(app_settings.get("auth_api_key"))
# print("auth api key:", app_settings.auth.api_key)
# print("auth local api key:", app_settings.auth.local.api_key)
# print(vars(app_settings))
