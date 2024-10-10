import logging
from typing import (
    Dict,
    Generator,
    List,
    Optional,
    Union,
)

from mergedeep import Strategy, merge

from probely.exceptions import (
    ProbelyBadRequest,
    ProbelyObjectNotFound,
    ProbelyRequestFailed,
)
from probely.sdk.enums import TargetAPISchemaTypeEnum, TargetTypeEnum
from probely.sdk.helpers import validate_resource_ids
from .client import ProbelyAPIClient
from ..settings import (
    PROBELY_API_PAGE_SIZE,
    PROBELY_API_TARGETS_BULK_DELETE_URL,
    PROBELY_API_TARGETS_BULK_UPDATE_URL,
    PROBELY_API_TARGETS_DELETE_URL,
    PROBELY_API_TARGETS_RETRIEVE_URL,
    PROBELY_API_TARGETS_URL,
)

logger = logging.getLogger(__name__)


def retrieve_targets(targets_ids: List[str]) -> List[Dict]:
    retrieved_targets = []
    for target_id in targets_ids:
        retrieved_targets.append(retrieve_target(target_id))

    return retrieved_targets


def retrieve_target(target_id: str) -> Dict:
    url = PROBELY_API_TARGETS_RETRIEVE_URL.format(id=target_id)
    resp_status_code, resp_content = ProbelyAPIClient.get(url)
    if resp_status_code == 404:
        raise ProbelyObjectNotFound(id=target_id)

    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content)

    return resp_content


def delete_target(target_id: str) -> str:
    url = PROBELY_API_TARGETS_DELETE_URL.format(id=target_id)

    resp_status_code, resp_content = ProbelyAPIClient.delete(url=url)

    if resp_status_code == 404:
        raise ProbelyObjectNotFound(id=target_id)

    if resp_status_code != 204:
        raise ProbelyRequestFailed(resp_content)

    return target_id


def delete_targets(targets_ids: List[str]):
    """Delete targets

    :param targets_ids: targets to be deleted.
    :type targets_ids: List[str].

    """
    validate_resource_ids(PROBELY_API_TARGETS_URL, targets_ids)

    url = PROBELY_API_TARGETS_BULK_DELETE_URL

    logger.debug("Delete targets : %s", targets_ids)
    resp_status_code, resp_content = ProbelyAPIClient.post(
        url=url, payload={"ids": targets_ids}
    )
    if resp_status_code != 200:
        raise ProbelyRequestFailed(resp_content)
    logger.debug("Targets : %s deleted successfully", targets_ids)
    return resp_content


def list_targets(targets_filters: Optional[Dict] = None) -> Generator[Dict, None, None]:
    filters = targets_filters or {}
    page = 1

    while True:
        query_params = {
            "ordering": "-changed",
            "length": PROBELY_API_PAGE_SIZE,
            "page": page,
            **filters,
        }

        resp_status_code, resp_content = ProbelyAPIClient.get(
            PROBELY_API_TARGETS_URL,
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


def add_target(
    target_url: str,
    target_name: Union[str, None] = None,
    target_type: TargetTypeEnum = TargetTypeEnum.WEB,
    api_schema_file_url: Union[str, None] = None,
    api_schema_type: Union[TargetAPISchemaTypeEnum, None] = None,
    extra_payload: Union[dict, None] = None,
) -> Dict:
    """Creates new target

    :param api_schema_type:
    :type api_schema_type: APISchemaTypeEnum, optional.
    :param api_schema_file_url:
    :type api_schema_file_url: str, optional.
    :param target_type:
    :type target_type: TargetTypeEnum, optional.
    :param target_url: url to be scanned.
    :type target_url: str.
    :param target_name: name of target.
    :type target_name: str, optional.
    :param extra_payload: allows customization of request. Content should follow api request body
    :type extra_payload: Optional[dict].
    :raise: ProbelyBadRequest.
    :return: Created target content.

    """
    create_target_url = PROBELY_API_TARGETS_URL

    query_params = {
        "duplicate_check": False,
        "skip_reachability_check": True,
    }

    body_data = {}
    if extra_payload:
        body_data = extra_payload

    arguments_settings = {
        "site": {"url": target_url},
        "type": target_type.api_request_value,
    }
    if target_name:
        arguments_settings["site"]["name"] = target_name

    if target_type == TargetTypeEnum.API:
        api_scan_settings = {}

        if api_schema_file_url:
            api_scan_settings["api_schema_url"] = api_schema_file_url

        if api_schema_type:
            api_scan_settings["api_schema_type"] = api_schema_type.api_request_value

        arguments_settings["site"]["api_scan_settings"] = api_scan_settings

    merge(body_data, arguments_settings, strategy=Strategy.REPLACE)

    resp_status_code, resp_content = ProbelyAPIClient.post(
        url=create_target_url, query_params=query_params, payload=body_data
    )

    if resp_status_code == 400:
        raise ProbelyBadRequest(response_payload=resp_content)

    if resp_status_code != 201:
        raise ProbelyRequestFailed(resp_content)

    created_target = resp_content
    return created_target


def update_target(target_id: str, payload: Dict) -> Dict:
    url = PROBELY_API_TARGETS_RETRIEVE_URL.format(id=target_id)

    resp_status_code, resp_content = ProbelyAPIClient.patch(url, payload=payload)

    if resp_status_code != 200:
        if resp_status_code == 400:
            raise ProbelyBadRequest(resp_content)
        if resp_status_code == 404:
            raise ProbelyObjectNotFound(id=target_id)
        raise ProbelyRequestFailed(resp_content)

    return resp_content


def update_targets(target_ids: List[str], payload: Dict) -> List[Dict]:
    validate_resource_ids(PROBELY_API_TARGETS_URL, target_ids)

    url = PROBELY_API_TARGETS_BULK_UPDATE_URL
    update_payload = {"ids": target_ids, **payload}

    resp_status_code, resp_content = ProbelyAPIClient.post(url, payload=update_payload)

    if resp_status_code != 200:
        if resp_status_code == 400:
            raise ProbelyBadRequest(resp_content)
        raise ProbelyRequestFailed(resp_content)

    # Bulk update returns only the IDs of the updated targets, so they need to be retrieved again
    targets_ids = resp_content.get("ids", [])
    targets = retrieve_targets(targets_ids)
    return targets
