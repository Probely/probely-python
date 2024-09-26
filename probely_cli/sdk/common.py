from urllib.parse import urljoin

from probely_cli.exceptions import ProbelyObjectNotFound
from probely_cli.sdk.client import ProbelyAPIClient
from probely_cli.utils import ProbelyCLIEnum


def validate_resource_ids(base_url: str, ids: list) -> None:
    """
    Validates a list of resource IDs by performing a GET request to the API.
    """
    for resource_id in ids:
        url = urljoin(base_url, resource_id)
        resp_status_code, _ = ProbelyAPIClient.get(url)
        if resp_status_code != 200:
            raise ProbelyObjectNotFound(id=resource_id)


class TargetRiskEnum(ProbelyCLIEnum):
    NA = (None, "null")
    NO_RISK = (0, "0")
    LOW = (10, "10")
    MEDIUM = (20, "20")
    HIGH = (30, "30")


class TargetTypeEnum(ProbelyCLIEnum):
    WEB = "single"
    API = "api"


class FindingSeverityEnum(ProbelyCLIEnum):
    LOW = (TargetRiskEnum.LOW.value, TargetRiskEnum.LOW.api_filter_value)
    MEDIUM = (TargetRiskEnum.MEDIUM.value, TargetRiskEnum.MEDIUM.api_filter_value)
    HIGH = (TargetRiskEnum.HIGH.value, TargetRiskEnum.HIGH.api_filter_value)


class FindingStateEnum(ProbelyCLIEnum):
    FIXED = "fixed"
    NOT_FIXED = "notfixed"
    ACCEPTED = "accepted"
    RETESTING = "retesting"


class APISchemaTypeEnum(ProbelyCLIEnum):
    OPENAPI = "openapi"
    POSTMAN = "postman"


class ScanStatusEnum(ProbelyCLIEnum):
    CANCELED = "canceled"
    CANCELING = "canceling"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    PAUSING = "pausing"
    QUEUED = "queued"
    RESUMING = "resuming"
    STARTED = "started"
    UNDER_REVIEW = "under_review"
    FINISHING_UP = "finishing_up"
