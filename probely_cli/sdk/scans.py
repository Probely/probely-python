import logging

from probely_cli.exceptions import ProbelyRequestFailed
from probely_cli.sdk.client import ProbelyAPICaller
from probely_cli.settings import get_scan_target_url

logger = logging.getLogger(__name__)


def start_scan(target_id: str, extra_payload: dict = None) -> dict:
    scan_target_url = get_scan_target_url(target_id)

    status_code, resp_content = ProbelyAPICaller().post(scan_target_url, extra_payload)

    if status_code != 200:
        logging.debug(
            "Request unsuccessful. Status code: {}, body: {}".format(
                status_code, resp_content
            )
        )
        raise ProbelyRequestFailed(resp_content)

    scan = resp_content
    return scan
