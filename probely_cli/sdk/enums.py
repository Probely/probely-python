from enum import Enum


class ProbelyCLIEnum(Enum):
    def __init__(self, api_response_value, api_filter_value=None):
        self._value_ = api_response_value
        self._api_filter_value = api_filter_value or api_response_value

    @property
    def api_filter_value(self):
        return self._api_filter_value

    @property
    def api_response_value(self):
        return self.value

    @property
    def api_request_value(self):
        return self.value

    @classmethod
    def get_by_api_response_value(cls, value):
        for enum_element in cls:
            if enum_element.value == value:
                return enum_element

        raise ValueError("{} is not a valid {}".format(value, cls.__name__))

    @classmethod
    def get_by_api_filter_value(cls, api_filter_value):
        for enum_element in cls:
            if enum_element._api_filter_value == api_filter_value:
                return enum_element

        raise ValueError("{} is not a valid {}".format(api_filter_value, cls.__name__))

    @classmethod
    def cli_input_choices(cls):
        input_choices = [enum_element.name for enum_element in cls]
        return input_choices


class TargetRiskEnum(ProbelyCLIEnum):
    NA = (None, "null")
    NO_RISK = (0, "0")
    LOW = (10, "10")
    MEDIUM = (20, "20")
    HIGH = (30, "30")


class TargetTypeEnum(ProbelyCLIEnum):
    WEB = "single"
    API = "api"


class TargetAPISchemaTypeEnum(ProbelyCLIEnum):
    OPENAPI = "openapi"
    POSTMAN = "postman"


class FindingSeverityEnum(ProbelyCLIEnum):
    LOW = (TargetRiskEnum.LOW.value, TargetRiskEnum.LOW.api_filter_value)
    MEDIUM = (TargetRiskEnum.MEDIUM.value, TargetRiskEnum.MEDIUM.api_filter_value)
    HIGH = (TargetRiskEnum.HIGH.value, TargetRiskEnum.HIGH.api_filter_value)


class FindingStateEnum(ProbelyCLIEnum):
    FIXED = "fixed"
    NOT_FIXED = "notfixed"
    ACCEPTED = "accepted"
    RETESTING = "retesting"


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
