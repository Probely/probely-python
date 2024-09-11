import logging
from typing import Dict, List
from urllib.parse import urljoin

from probely_cli.exceptions import ProbelyObjectNotFound, ProbelyRequestFailed
from probely_cli.sdk.client import ProbelyAPIClient
from probely_cli.settings import (
    PROBELY_API_SCANS_BULK_CANCEL_URL,
    PROBELY_API_SCANS_BULK_RESUME_URL,
    PROBELY_API_SCANS_URL,
    PROBELY_API_START_SCAN_URL,
)

logger = logging.getLogger(__name__)


def start_scan(target_id: str, extra_payload: dict = None) -> dict:
    scan_target_url = PROBELY_API_START_SCAN_URL.format(target_id=target_id)

    resp_status_code, resp_content = ProbelyAPIClient().post(
        scan_target_url, extra_payload
    )

    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content)

    scan = resp_content
    return scan


def cancel_scans(scan_ids: List[str]) -> List[dict]:
    scan_cancel_url = PROBELY_API_SCANS_BULK_CANCEL_URL

    resp_status_code, resp_content = ProbelyAPIClient().post(
        scan_cancel_url, {"scans": [{"id": scan_id} for scan_id in scan_ids]}
    )

    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content)

    scans = resp_content
    return scans


def list_scans(scans_filters: Dict = None) -> List[Dict]:
    """Lists existing Account's Scans

    :return: All Scans of Account
    :rtype: List[Dict]
    """
    filters = scans_filters or {}

    query_params = {
        "length": 50,
        "ordering": "-changed",
        "page": 1,
        **filters,
    }

    resp_status_code, resp_content = ProbelyAPIClient().get(
        PROBELY_API_SCANS_URL,
        query_params=query_params,
    )

    if resp_status_code != 200:  # TODO: needs testing
        raise ProbelyRequestFailed(resp_content)

    return resp_content["results"]


def retrieve_scan(scan_id: str) -> dict:
    url = urljoin(PROBELY_API_SCANS_URL, scan_id)

    resp_status_code, resp_content = ProbelyAPIClient().get(url)
    if resp_status_code == 404:
        raise ProbelyObjectNotFound(id=scan_id)
    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content)

    return resp_content


def retrieve_scans(scan_ids: List[str]) -> List[Dict]:
    return [retrieve_scan(scan_id) for scan_id in scan_ids]


def resume_scans(scan_ids: List[str], ignore_blackout_period=False) -> List[Dict]:
    scan_resume_url = PROBELY_API_SCANS_BULK_RESUME_URL

    scans = []
    for scan_id in scan_ids:
        scan = retrieve_scan(scan_id)
        scans.append(scan)

    payload = {
        "scans": [{"id": scan_id} for scan_id in scan_ids],
        "overrides": {"ignore_blackout_period": ignore_blackout_period},
    }

    resp_status_code, resp_content = ProbelyAPIClient().post(scan_resume_url, payload)

    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content, resp_status_code)

    return scans


def resume_scan(scan_id: str, ignore_blackout_period=False) -> dict:
    scan = resume_scans([scan_id], ignore_blackout_period)[0]
    return scan
