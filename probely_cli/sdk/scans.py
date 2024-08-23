import logging

from probely_cli.exceptions import ProbelyRequestFailed
from probely_cli.sdk.client import ProbelyAPIClient
from probely_cli.settings import PROBELY_API_SCANS_URL

logger = logging.getLogger(__name__)


def start_scan(target_id: str, extra_payload: dict = None) -> dict:
    scan_target_url = PROBELY_API_SCANS_URL.format(target_id=target_id)

    resp_status_code, resp_content = ProbelyAPIClient().post(
        scan_target_url, extra_payload
    )

    if resp_status_code != 200:
        logging.debug(
            "Request unsuccessful. Status code: {}, body: {}".format(
                resp_status_code, resp_content
            )
        )
        raise ProbelyRequestFailed(resp_content)

    scan = resp_content
    return scan
