import json
import logging
from typing import List, Dict

from mergedeep import merge, Strategy
from requests import sessions, Request

from .client import _get_client
from probely_cli.exceptions import ProbelyRequestFailed, ProbelyBadRequest
from ..settings import PROBELY_API_TARGETS_URL


logger = logging.getLogger(__name__)


def list_targets() -> List[Dict]:
    """Lists existing account's targets

    :return: All Targets of account
    :rtype: List[Dict]

    """
    # TODO: go through pagination
    # or maybe the option to return a generator for the sdk??
    r = _get_client().get(PROBELY_API_TARGETS_URL)

    output = json.loads(r.content)

    if r.status_code != 200:
        raise ProbelyRequestFailed(output["detail"])

    return output["results"]


def add_target(
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
    session: sessions.Session = _get_client()
    prepared_request = session.prepare_request(
        Request("post", url=create_target_url, json=body_data)
    )

    resp = session.send(prepared_request)
    output = json.loads(resp.content)

    logger.debug("Add target request response code: %s", resp.status_code)
    if resp.status_code == 400:
        ex = ProbelyBadRequest(response_payload=output)
        raise ex

    if resp.status_code != 201:
        raise ProbelyRequestFailed(output["detail"])

    created_target = output
    return created_target
