from enum import Enum

from probely_cli.sdk.enums import ProbelyCLIEnum


class EntityTypeEnum(Enum):
    SCAN = "scan"
    FINDING = "finding"
    TARGET = "target"


class OutputEnum(ProbelyCLIEnum):
    YAML = "yaml"
    JSON = "json"
