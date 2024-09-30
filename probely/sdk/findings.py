from typing import (
    Dict,
    Generator,
    List,
    Optional,
)

from probely.exceptions import ProbelyObjectNotFound, ProbelyRequestFailed
from probely.sdk.client import ProbelyAPIClient
from probely.settings import (
    PROBELY_API_FINDINGS_RETRIEVE_URL,
    PROBELY_API_FINDINGS_URL,
    PROBELY_API_PAGE_SIZE,
)


def retrieve_finding(finding_id) -> Dict:
    url = PROBELY_API_FINDINGS_RETRIEVE_URL.format(id=finding_id)
    resp_status_code, resp_content = ProbelyAPIClient.get(url)

    if resp_status_code == 404:
        raise ProbelyObjectNotFound(id=finding_id)

    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content)

    return resp_content


def retrieve_findings(findings_ids: List[str]) -> List[Dict]:
    return [retrieve_finding(finding_id) for finding_id in findings_ids]


def list_findings(
    findings_filters: Optional[Dict] = None,
) -> Generator[Dict, None, None]:
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

        if page >= total_pages_count:
            break

        page += 1
