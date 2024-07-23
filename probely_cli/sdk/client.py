import json
import logging
from urllib.parse import urlencode

import requests
from requests import Request, Session

from probely_cli import settings
from probely_cli.exceptions import ProbelyMissConfig, ProbelyApiUnavailable

logger = logging.getLogger(__name__)


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


class ProbelyAPIClient:

    def get(self, url, query_params=None):
        if query_params:
            url = f"{url}?{urlencode(query_params)}"

        request = Request("get", url=url)

        return self._call_probely_api(request)

    def post(self, url, payload: dict = None):
        if payload is None:
            payload = {}

        logger.debug("Requesting probely API. Payload: {}".format(payload))
        request = Request("post", url=url, json=payload)

        return self._call_probely_api(request)

    # noinspection PyMethodMayBeStatic
    def _call_probely_api(self, request):
        session: Session = self._build_session()
        prepared_request = session.prepare_request(request)

        logger.debug("Requesting probely API in {}".format(prepared_request.url))
        resp = session.send(prepared_request)

        status_code = resp.status_code
        try:
            content = json.loads(resp.content)
        except json.JSONDecodeError:  # todo: needs testing
            print(resp.content)
            logger.debug(
                "Something wrong with the API. Response content is not valid JSON."
            )
            raise ProbelyApiUnavailable

        logger.debug(f"Response content: {content}")

        return status_code, content

    # noinspection PyMethodMayBeStatic
    def _build_session(self) -> requests.Session:
        session = requests.Session()
        api_key = Probely().APP_CONFIG["api_key"]

        debug_message = (
            "Session setup with api_key ************{}".format(api_key[-4:])
            if api_key
            else "No API Key provided"
        )
        logger.debug(debug_message)

        session.headers.update({"Authorization": "JWT " + api_key})
        return session
