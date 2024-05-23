import json

from probely_cli.exceptions import ProbelyRequestFailed
from probely_cli.sdk.client import _get_client
from probely_cli.settings import get_scan_target_url


def start_scan(target_id):
    scan_target_url = get_scan_target_url(target_id)
    r = _get_client().post(scan_target_url)

    output = json.loads(r.content)

    if r.status_code != 200:
        print("meh?")
        raise ProbelyRequestFailed(output)

    scan = output
    return scan
