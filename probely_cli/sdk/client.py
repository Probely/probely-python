import requests
from probely_cli import settings


def init(api_key):  # how many settings are we gonna support?
    # sentry_sdk.init(dsn="ehdllo")
    pass


def _get_client(api_key=None):
    session = requests.Session()
    print(f"[{__name__}]---", "api key:", settings.PROBELY_API_KEY)
    session.headers.update({"Authorization": "JWT " + settings.PROBELY_API_KEY})

    return session


probely_client: requests.Session = _get_client()
