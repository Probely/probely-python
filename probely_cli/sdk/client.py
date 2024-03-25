import requests
from probely_cli import settings
from probely_cli.exceptions import ProbelyMissConfig


class Probely:
    _instance = None
    APP_CONFIG: dict = dict()

    def __init__(self, api_key=None, *args, **kwargs):
        if self.APP_CONFIG.get("is_app_configured", None):
            return

        self.APP_CONFIG = {
            "is_app_configured": True,
            "api_key": settings.PROBELY_API_KEY,
        }

        if api_key:
            self.APP_CONFIG["api_key"] = api_key

        self._validate_config()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            instance = super().__new__(cls, *args, **kwargs)
            cls._instance = instance
        return cls._instance

    def _validate_config(self):
        if self.APP_CONFIG["api_key"] is None:
            raise ProbelyMissConfig("Missing fundamental config: api_key")

    @classmethod
    def init(cls, *args, **kwargs):
        instance = cls()
        instance.APP_CONFIG["is_app_configured"] = False
        instance.__init__(*args, **kwargs)


def _get_client() -> requests.Session:
    session = requests.Session()
    print("who am I?", session)
    api_key = Probely().APP_CONFIG["api_key"]

    session.headers.update({"Authorization": "JWT " + api_key})
    return session
