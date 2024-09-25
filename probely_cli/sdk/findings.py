from typing import Generator, List, Dict

from probely_cli.exceptions import ProbelyRequestFailed, ProbelyObjectNotFound
from probely_cli.sdk.client import ProbelyAPIClient
from probely_cli.settings import (
    PROBELY_API_FINDINGS_URL,
    PROBELY_API_FINDINGS_RETRIEVE_URL,
    PROBELY_API_PAGE_SIZE,
)


def retrieve_findings(findings_ids: List[str]) -> List[Dict]:
    findings = []
    for target_id in findings_ids:
        finding = retrieve_finding(target_id)
        findings.append(finding)
    return findings


def retrieve_finding(finding_id) -> dict:
    url = PROBELY_API_FINDINGS_RETRIEVE_URL.format(id=finding_id)
    resp_status_code, resp_content = ProbelyAPIClient.get(url)

    if resp_status_code == 404:
        raise ProbelyObjectNotFound(id=finding_id)

    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content)

    return resp_content


def list_findings(findings_filters: Dict = None) -> Generator[Dict, None, None]:
    filters = findings_filters or {}
    page = 1

    while True:
        query_params = {
            "ordering": "-last_found",
            "length": PROBELY_API_PAGE_SIZE,
            "page": page,
            **filters,
        }

        resp_status_code, resp_content = ProbelyAPIClient.get(
            PROBELY_API_FINDINGS_URL,
            query_params=query_params,
        )

        if resp_status_code != 200:
            raise ProbelyRequestFailed(resp_content)

        results = resp_content["results"]
        total_pages_count = resp_content.get("page_total")

        for result in results:
            yield result

        if total_pages_count >= page:
            break

        page += 1
