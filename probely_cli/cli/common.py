from pathlib import Path
from typing import Type

import marshmallow
import yaml
from marshmallow import post_load

import probely_cli.settings as settings
from probely_cli.exceptions import ProbelyCLIValidation
from probely_cli.utils import ProbelyCLIEnum


def lowercase_acceptable_parser_type(value: str):
    return value.upper()


def show_help(args):
    if args.is_no_action_parser:
        args.cli_parser.print_help()


def validate_and_retrieve_yaml_content(yaml_file_path):
    file_path = Path(yaml_file_path)

    if not file_path.exists():
        raise ProbelyCLIValidation("Provided path does not exist: {}".format(file_path))

    if not file_path.is_file():
        raise ProbelyCLIValidation(
            "Provided path is not a file: {}".format(file_path.absolute())
        )

    if file_path.suffix not in settings.CLI_ACCEPTED_FILE_EXTENSIONS:
        raise ProbelyCLIValidation(
            "Invalid file extension, must be one of the following: {}:".format(
                settings.CLI_ACCEPTED_FILE_EXTENSIONS
            )
        )

    with file_path.open() as yaml_file:
        try:
            # TODO: supported yaml versions?
            yaml_content = yaml.safe_load(yaml_file)
        except yaml.scanner.ScannerError as ex:
            raise ProbelyCLIValidation("Invalid yaml content in file: {}".format(ex))

    return yaml_content


class TargetRiskEnum(ProbelyCLIEnum):
    NA = (None, "null")
    NO_RISK = (0, "0")
    LOW = (10, "10")
    NORMAL = (20, "20")
    HIGH = (30, "30")


class TargetTypeEnum(ProbelyCLIEnum):
    WEB = "single"
    API = "api"


class FindingSeverityEnum(ProbelyCLIEnum):
    LOW = (TargetRiskEnum.LOW.value, TargetRiskEnum.LOW.api_filter_value)
    NORMAL = (TargetRiskEnum.NORMAL.value, TargetRiskEnum.NORMAL.api_filter_value)
    HIGH = (TargetRiskEnum.HIGH.value, TargetRiskEnum.HIGH.api_filter_value)


class FindingStateEnum(ProbelyCLIEnum):
    FIXED = "fixed"
    NOT_FIXED = "notfixed"
    ACCEPTED = "accepted"
    RETESTING = "retesting"


class OutputEnum(ProbelyCLIEnum):
    YAML = "yaml"
    JSON = "json"


class ProbelyCLIBaseFiltersSchema(marshmallow.Schema):
    @post_load
    def ignore_unused_filters(self, data, **kwargs):
        """
        All argparse arguments default to None, which means they must be removed.
        This avoids errors when calling the API.
        """
        command_filters = {f: v for f, v in data.items() if v is not None}
        return command_filters

    class Meta:
        # ignores other args that are not filters
        unknown = marshmallow.EXCLUDE


class ProbelyCLIEnumField(marshmallow.fields.Enum):
    enum_class: Type[ProbelyCLIEnum]

    def __init__(self, enum_class: Type[ProbelyCLIEnum], *args, **kwargs):
        self.enum_class = enum_class
        super().__init__(enum=enum_class, *args, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        raise NotImplementedError()

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return self.enum_class[value].api_filter_value
        except:
            raise marshmallow.ValidationError("Values not within the accepted values.")


