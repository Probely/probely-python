import os

import requests

from probely_cli import settings

_API_KEY = os.environ.get("PROBELY_API_KEY")
_INIT_API_KEY = None


def init(api_key):  # how many settings are we gonna support?
    # sentry_sdk.init(dsn="ehdllo")
    pass


def _get_client():
    session = requests.Session()
    session.headers.update({"Authorization": settings.PROBELY_API_TOKEN})

    return session


probely_client: requests.Session = _get_client()
