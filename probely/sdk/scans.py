import logging
from typing import (
    Dict,
    Generator,
    List,
    Optional,
)
from urllib.parse import urljoin

from probely.exceptions import (
    ProbelyBadRequest,
    ProbelyObjectNotFound,
    ProbelyRequestFailed,
)
from probely.sdk.client import ProbelyAPIClient
from probely.sdk.helpers import validate_resource_ids
from probely.settings import (
    PROBELY_API_SCANS_BULK_START_URL,
    PROBELY_API_PAGE_SIZE,
    PROBELY_API_SCAN_CANCEL_URL,
    PROBELY_API_SCAN_PAUSE_URL,
    PROBELY_API_SCAN_RESUME_URL,
    PROBELY_API_SCANS_BULK_CANCEL_URL,
    PROBELY_API_SCANS_BULK_PAUSE_URL,
    PROBELY_API_SCANS_BULK_RESUME_URL,
    PROBELY_API_SCANS_URL,
    PROBELY_API_TARGETS_START_SCAN_URL,
    PROBELY_API_TARGETS_URL,
)

logger = logging.getLogger(__name__)


def start_scan(target_id: str, extra_payload: dict = None) -> dict:
    scan_target_url = PROBELY_API_TARGETS_START_SCAN_URL.format(target_id=target_id)

    resp_status_code, resp_content = ProbelyAPIClient.post(
        scan_target_url, payload=extra_payload
    )

    if resp_status_code != 200:
        if resp_status_code == 400:
            raise ProbelyBadRequest(resp_content)
        if resp_status_code == 404:
            raise ProbelyObjectNotFound(id=target_id)
        raise ProbelyRequestFailed(resp_content)

    scan = resp_content
    return scan


def start_scans(target_ids: List[str], extra_payload: Dict = None) -> List[Dict]:
    validate_resource_ids(PROBELY_API_TARGETS_URL, target_ids)

    url = PROBELY_API_SCANS_BULK_START_URL
    extra_payload = extra_payload or {}

    payload = {
        "targets": [{"id": target_id} for target_id in target_ids],
        **extra_payload,
    }

    resp_status_code, resp_content = ProbelyAPIClient.post(url, payload=payload)

    if resp_status_code == 400:
        raise ProbelyBadRequest(resp_content)

    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content)

    scans = resp_content
    return scans


def cancel_scans(scan_ids: List[str]) -> List[Dict]:
    scan_cancel_url = PROBELY_API_SCANS_BULK_CANCEL_URL

    for scan_id in scan_ids:
        retrieve_scan(scan_id)

    payload = {"scans": [{"id": scan_id} for scan_id in scan_ids]}

    resp_status_code, resp_content = ProbelyAPIClient.post(
        scan_cancel_url, payload=payload
    )

    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content)

    scans = []
    for scan_id in scan_ids:
        scan = retrieve_scan(scan_id)
        scans.append(scan)

    return scans


def cancel_scan(scan_id: str) -> dict:
    scan = retrieve_scan(scan_id)
    target = scan.get("target", {})

    scan_cancel_url = PROBELY_API_SCAN_CANCEL_URL.format(
        target_id=target.get("id"), scan_id=scan_id
    )

    payload = {
        "target_options": {
            "site": target.get("site"),
            "scanning_agent": target.get("scanning_agent"),
        },
        "has_sequence_navigation": scan.get("has_sequence_navigation"),
        "user_data": scan.get("user_data"),
    }

    resp_status_code, resp_content = ProbelyAPIClient.post(
        scan_cancel_url,
        payload=payload,
    )

    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content, resp_status_code)

    return resp_content


def pause_scan(scan_id: str) -> Dict:
    scan = retrieve_scan(scan_id)
    target = scan.get("target", {})

    scan_pause_url = PROBELY_API_SCAN_PAUSE_URL.format(
        target_id=target.get("id"), scan_id=scan_id
    )

    payload = {
        "target_options": {
            "site": target.get("site"),
            "scanning_agent": target.get("scanning_agent"),
        },
        "has_sequence_navigation": scan.get("has_sequence_navigation"),
        "user_data": scan.get("user_data"),
    }

    resp_status_code, resp_content = ProbelyAPIClient.post(
        scan_pause_url,
        payload=payload,
    )

    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content, resp_status_code)

    return resp_content


def pause_scans(scan_ids: List[str]) -> List[Dict]:
    scan_pause_url = PROBELY_API_SCANS_BULK_PAUSE_URL

    for scan_id in scan_ids:
        scan = retrieve_scan(scan_id)

    payload = {"scans": [{"id": scan_id} for scan_id in scan_ids]}

    resp_status_code, resp_content = ProbelyAPIClient.post(
        scan_pause_url,
        payload=payload,
    )

    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content, resp_status_code)

    scans = []
    for scan_id in scan_ids:
        scan = retrieve_scan(scan_id)
        scans.append(scan)

    return scans


def resume_scan(scan_id: str) -> Dict:
    scan = retrieve_scan(scan_id)
    target = scan.get("target", {})

    scan_resume_url = PROBELY_API_SCAN_RESUME_URL.format(
        target_id=target.get("id"), scan_id=scan_id
    )

    payload = {
        "target_options": {
            "site": target.get("site"),
            "scanning_agent": target.get("scanning_agent"),
        },
        "has_sequence_navigation": scan.get("has_sequence_navigation"),
        "user_data": scan.get("user_data"),
    }

    resp_status_code, resp_content = ProbelyAPIClient.post(
        scan_resume_url,
        payload=payload,
    )

    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content, resp_status_code)

    return resp_content


def resume_scans(scan_ids: List[str], ignore_blackout_period=False) -> List[Dict]:
    scan_resume_url = PROBELY_API_SCANS_BULK_RESUME_URL

    for scan_id in scan_ids:
        retrieve_scan(scan_id)

    payload = {
        "scans": [{"id": scan_id} for scan_id in scan_ids],
        "overrides": {"ignore_blackout_period": ignore_blackout_period},
    }

    resp_status_code, resp_content = ProbelyAPIClient.post(
        scan_resume_url, payload=payload
    )

    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content, resp_status_code)

    scans = []
    for scan_id in scan_ids:
        scan = retrieve_scan(scan_id)
        scans.append(scan)

    return scans


def retrieve_scan(scan_id: str) -> Dict:
    url = urljoin(PROBELY_API_SCANS_URL, scan_id)

    resp_status_code, resp_content = ProbelyAPIClient.get(url)
    if resp_status_code == 404:
        raise ProbelyObjectNotFound(id=scan_id)
    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content)

    return resp_content


def retrieve_scans(scan_ids: List[str]) -> List[Dict]:
    return [retrieve_scan(scan_id) for scan_id in scan_ids]


def list_scans(scans_filters: Optional[Dict] = None) -> Generator[Dict, None, None]:
    filters = scans_filters or {}
    page = 1

    while True:
        query_params = {
            "ordering": "-changed",
            "length": PROBELY_API_PAGE_SIZE,
            "page": page,
            **filters,
        }

        resp_status_code, resp_content = ProbelyAPIClient.get(
            PROBELY_API_SCANS_URL,
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
