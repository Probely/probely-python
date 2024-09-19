import json
import sys
from pathlib import Path
from typing import Type, Union

import dateutil.parser
import marshmallow
import yaml
from marshmallow import post_load

import probely_cli.settings as settings
from probely_cli.exceptions import ProbelyCLIValidation
from probely_cli.utils import ProbelyCLIEnum


def show_help(args):
    if args.is_no_action_parser:
        args.parser.print_help()


def validate_and_retrieve_yaml_content(yaml_file_path: Union[str, None]):
    if not yaml_file_path:
        return dict()

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
            if yaml_content is None:
                raise ProbelyCLIValidation("YAML file {} is empty.".format(file_path))
        except yaml.error.YAMLError as ex:
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


class APISchemaTypeEnum(ProbelyCLIEnum):
    OPENAPI = "openapi"
    POSTMAN = "postman"


class OutputEnum(ProbelyCLIEnum):
    YAML = "yaml"
    JSON = "json"


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


class ISO8601DateTimeField(marshmallow.fields.Field):
    """
    Field for parsing ISO 8601 datetime strings into datetime objects and serializing them back.

    An ISO-8601 datetime string consists of a date portion, followed optionally by a time
    portion - the date and time portions are separated by a single character separator,
    which is ``T`` in the official standard.

    Supported common date formats are:
    - ``YYYY``
    - ``YYYY-MM``
    - ``YYYY-MM-DD`` or ``YYYYMMDD``

    Supported common time formats are:
    - ``hh``
    - ``hh:mm`` or ``hhmm``
    - ``hh:mm:ss`` or ``hhmmss``
    - ``hh:mm:ss.ssssss`` (Up to 6 sub-second digits)
    """

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return dateutil.parser.isoparse(value)
        except (ValueError, TypeError, OverflowError):
            raise marshmallow.ValidationError(
                "Invalid datetime format. Please provide a valid datetime in ISO 8601 format."
            )

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.isoformat()


def display_scans_response_output(args, scans):
    """
    Args:
        args: Command-line arguments that include output format (optional) and console for printing.
              It is expected to have an 'output' attribute indicating the desired format and a 'console' attribute for printing.
        scans: The list of scans to be formatted and displayed.

    Output:
        The formatted scans is printed to the console in the specified format (JSON, YAML), or in a default format.
    """

    output_type = OutputEnum[args.output] if args.output else None

    if not output_type:
        for scan in scans:
            args.console.print(scan["id"])
        return

    if output_type == OutputEnum.JSON:
        output = json.dumps(scans, indent=2)
    else:
        output = yaml.dump(scans, indent=2, width=sys.maxsize)

    args.console.print(output)
