from typing import List, Dict

from probely_cli.exceptions import ProbelyRequestFailed, ProbelyObjectNotFound
from probely_cli.sdk.client import ProbelyAPIClient
from probely_cli.settings import (
    PROBELY_API_FINDINGS_URL,
    PROBELY_API_FINDINGS_RETRIEVE_URL,
)


def retrieve_findings(findings_ids: List[str]) -> List[Dict]:
    retrieved_findings = []
    for target_id in findings_ids:
        retrieved_findings.append(retrieve_finding(target_id))

    return retrieved_findings


def retrieve_finding(finding_id) -> dict:
    url = PROBELY_API_FINDINGS_RETRIEVE_URL.format(id=finding_id)
    resp_status_code, resp_content = ProbelyAPIClient().get(url)

    if resp_status_code == 404:
        raise ProbelyObjectNotFound(id=finding_id)

    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content)

    return resp_content


def list_findings(findings_filters: dict = None) -> List[Dict]:
    filters = findings_filters or {}

    query_params = {
        "length": 100,
        "ordering": "-last_found",
        "page": 1,
        **filters,
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
