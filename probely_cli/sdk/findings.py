from typing import List, Dict

from probely_cli.exceptions import ProbelyRequestFailed
from probely_cli.sdk.client import ProbelyAPIClient
from probely_cli.settings import PROBELY_API_FINDINGS_URL


def list_findings() -> List[Dict]:

    query_params = {
        "length": 100,
        "ordering": "-last_found",
        "page": 1,
    }

    # TODO: go through pagination?
    # or maybe the option to return a generator for the sdk??
    resp_status_code, resp_content = ProbelyAPIClient().get(
        PROBELY_API_FINDINGS_URL,
        query_params=query_params,
    )

    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content)

    return resp_content["results"]
