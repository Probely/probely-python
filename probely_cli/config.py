import os

import requests
import sentry_sdk
import settings

_API_KEY = os.environ.get("PROBELY_API_KEY")
_INIT_API_KEY = None


def init(api_key):  # how many settings are we gonna support?
    sentry_sdk.init(dsn="ehdllo")


def _get_client():
    print("client config running")
    session = requests.Session()
    session.headers.update({"Authorization": settings.QA_TOKEN})

    return session


probely_client: requests.Session = _get_client()
