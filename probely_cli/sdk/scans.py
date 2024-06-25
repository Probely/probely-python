import json
import logging

from requests import Request, Session

from probely_cli.exceptions import ProbelyRequestFailed
from probely_cli.sdk.client import _get_client
from probely_cli.settings import get_scan_target_url

logger = logging.getLogger(__name__)


class RequestProbely:
    def post(self, url, payload: dict = None):
        if payload is None:
            payload = {}

        logger.debug("Requesting probely. Payload: {}".format(payload))
        request = Request("post", url=url, json=payload)

        return self.send_request_probely(request)

    @staticmethod
    def send_request_probely(request):
        session: Session = _get_client()
        prepared_request = session.prepare_request(request)

        resp = session.send(prepared_request)

        status_code = resp.status_code
        try:
            content = json.loads(resp.content)
        except json.JSONDecodeError:
            logger.debug("Response content is not valid JSON. Contact support.")
            raise

        logger.debug(f"Response content: {content}")

        return status_code, content


def start_scan(target_id: str, extra_payload: dict = None) -> dict:
    scan_target_url = get_scan_target_url(target_id)

    status_code, resp_content = RequestProbely().post(scan_target_url, extra_payload)

    if status_code != 200:
        logging.debug(
            "Request failed. Status code: {}, body: {}".format(
                status_code, resp_content
            )
        )
        raise ProbelyRequestFailed(resp_content)

    scan = resp_content
    return scan
