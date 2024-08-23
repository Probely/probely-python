import logging
from typing import List, Dict

from mergedeep import merge, Strategy

from probely_cli.exceptions import (
    ProbelyRequestFailed,
    ProbelyBadRequest,
    ProbelyObjectNotFound,
)
from .client import ProbelyAPIClient
from ..settings import PROBELY_API_TARGETS_URL, PROBELY_API_TARGETS_RETRIEVE_URL

logger = logging.getLogger(__name__)


def retrieve_targets(targets_ids: List[str]) -> List[Dict]:
    retrieved_targets = []
    for target_id in targets_ids:
        retrieved_targets.append(retrieve_target(target_id))

    return retrieved_targets


def retrieve_target(target_id) -> dict:
    url = PROBELY_API_TARGETS_RETRIEVE_URL.format(id=target_id)
    resp_status_code, resp_content = ProbelyAPIClient().get(url)
    if resp_status_code == 404:
        raise ProbelyObjectNotFound(id=target_id)

    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content)

    return resp_content


def list_targets(targets_filters: dict = None) -> List[Dict]:
    """Lists existing account's targets

    :return: All Targets of account
    :rtype: List[Dict]

    """
    filters = targets_filters or {}

    query_params = {
        "length": 50,
        "ordering": "-changed",
        "page": 1,
        **filters,
    }

    # TODO: go through pagination?
    # or maybe the option to return a generator for the sdk??
    resp_status_code, resp_content = ProbelyAPIClient().get(
        PROBELY_API_TARGETS_URL,
        query_params=query_params,
    )

    if resp_status_code != 200:  # TODO: needs testing
        raise ProbelyRequestFailed(resp_content)

    return resp_content["results"]


def add_target(  # TODO: needs testing
    site_url: str,
    site_name: str = None,
    extra_payload: dict = None,
) -> Dict:
    """Creates new target

    :param site_url: url to be scanned.
    :type site_url: str.
    :param site_name: name of target.
    :type site_name: str, optional.
    :param extra_payload: allows customization of request. Content should follow api request body
    :type extra_payload: Optional[dict].
    :raise: ProbelyBadRequest.
    :return: Created target content.

    """

    create_target_url = (
        PROBELY_API_TARGETS_URL  # + "?duplicate_check=true&check_fullpath=true"
    )

    body_data = {}
    if extra_payload:
        body_data = extra_payload

    arguments_settings = {"site": {"url": site_url}}
    if site_name:
        arguments_settings["site"]["name"] = site_name

    merge(body_data, arguments_settings, strategy=Strategy.REPLACE)

    logger.debug("Add target request content: %s", body_data)
    resp_status_code, resp_content = ProbelyAPIClient().post(
        url=create_target_url, payload=body_data
    )

    logger.debug("Add target request response code: %s", resp_status_code)
    if resp_status_code == 400:
        ex = ProbelyBadRequest(response_payload=resp_content)
        raise ex

    if resp_status_code != 201:
        raise ProbelyRequestFailed(resp_content)

    created_target = resp_content
    return created_target
