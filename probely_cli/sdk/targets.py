import json
import logging
from typing import List, Dict

from requests import sessions, Request

from .client import _get_client
from ..exceptions import ProbelyRequestFailed, ProbelyBadRequest
from ..settings import PROBELY_API_TARGETS_URL


logger = logging.getLogger(__name__)


def list_targets() -> List[Dict]:
    # TODO: go through pagination
    # or maybe the option to return a generator for the sdk??
    r = _get_client().get(PROBELY_API_TARGETS_URL)

    output = json.loads(r.content)

    if r.status_code != 200:
        raise ProbelyRequestFailed(output["detail"])

    return output["results"]


def add_target(site_url: str, site_name: str) -> dict:
    create_target_url = (
        PROBELY_API_TARGETS_URL  # + "?duplicate_check=true&check_fullpath=true"
    )
    body_data = {"site": {"name": site_name, "url": site_url}}
    session: sessions.Session = _get_client()
    prepared_request = session.prepare_request(
        Request("post", url=create_target_url, json=body_data)
    )

    logger.debug("Add target request content: %s", body_data)
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
