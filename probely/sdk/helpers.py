from urllib.parse import urljoin

from probely.exceptions import ProbelyObjectNotFound
from probely.sdk.client import ProbelyAPIClient


def validate_resource_ids(base_url: str, ids: list) -> None:
    """
    Validates a list of resource IDs by performing a GET request to the API.
    """
    for resource_id in ids:
        url = urljoin(base_url, resource_id)
        resp_status_code, _ = ProbelyAPIClient.get(url)
        if resp_status_code != 200:
            raise ProbelyObjectNotFound(id=resource_id)
