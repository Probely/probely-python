from pathlib import Path
from typing import Dict, List, Union

import yaml
from dateutil import parser

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


class OutputEnum(ProbelyCLIEnum):
    YAML = "yaml"
    JSON = "json"


def get_printable_risk(api_risk_value) -> str:
    try:
        risk_name: str = TargetRiskEnum.get_by_api_response_value(api_risk_value).name
        return risk_name
    except ValueError:
        return "Unknown"  # TODO: scenario that risk enum updated but CLI is forgotten


def get_printable_labels(labels: List[Dict] = None) -> str:
    if labels is None:
        return "Unknown_labels"

    labels_name = []
    try:
        [labels_name.append(label["name"]) for label in labels]
    except:
        return "Unknown_labels"

    printable_labels = ", ".join(labels_name)

    return printable_labels


def get_printable_date(
    date_string: Union[str, None],
    default_string: Union[str, None] = None,
) -> str:
    if date_string:
        datetime = parser.isoparse(date_string)
        return datetime.strftime("%Y-%m-%d %H:%M")

    if default_string:
        return default_string

    return ""
