import argparse
import json
import logging
import sys
from typing import Optional

import yaml

from probely.cli.common import validate_and_retrieve_yaml_content
from probely.cli.enums import OutputEnum
from probely.exceptions import ProbelyCLIValidation
from probely.sdk.enums import TargetAPISchemaTypeEnum, TargetTypeEnum
from probely.sdk.targets import add_target

logger = logging.getLogger(__name__)


def build_cmd_output(args, target):
    output_type = OutputEnum[args.output] if args.output else None

    if output_type == OutputEnum.JSON:
        return json.dumps(target, indent=2)

    if output_type == OutputEnum.YAML:
        return yaml.dump(
            target,
            indent=2,
            width=sys.maxsize,  # avoids word wrapping
        )

    return target["id"]


def validate_and_retrieve_api_scan_settings(
    target_type, api_schema_file_url, api_schema_type
):
    api_schema_settings = dict()

    if target_type != TargetTypeEnum.API:
        return api_schema_settings

    has_schema_file = api_schema_file_url

    if not has_schema_file:
        msg = "API targets require api_schema_file_url"
        raise ProbelyCLIValidation(msg)

    if has_schema_file and not api_schema_type:
        raise ProbelyCLIValidation("API schema file require api_schema_type")

    api_schema_settings["api_schema_type"] = api_schema_type
    api_schema_settings["api_schema_file_url"] = api_schema_file_url

    return api_schema_settings


def get_target_type(args, file_input):
    if args.target_type:  # should be validated by argparse
        return TargetTypeEnum[args.target_type]

    if file_input.get("type", None):
        try:
            target_type = TargetTypeEnum.get_by_api_response_value(
                file_input.get("type")
            )
            return target_type
        except ValueError:
            raise ProbelyCLIValidation(
                "target type '{}' from file is not a valid options".format(
                    file_input["type"]
                )
            )

    return TargetTypeEnum.WEB


def get_api_schema_type(args, file_input):
    if args.api_schema_type:
        return TargetAPISchemaTypeEnum[args.api_schema_type]

    api_schema_type_from_file: Optional[str] = (
        file_input.get("site", {})
        .get("api_scan_settings", {})
        .get("api_schema_type", None)
    )

    if api_schema_type_from_file:
        try:
            return TargetAPISchemaTypeEnum.get_by_api_response_value(
                api_schema_type_from_file
            )
        except ValueError:
            validation_msg = "API schema type '{}' from file is not a valid options"
            raise ProbelyCLIValidation(validation_msg.format(api_schema_type_from_file))

    return None


def get_command_arguments(args: argparse.Namespace):
    file_input = validate_and_retrieve_yaml_content(args.yaml_file_path)
    command_arguments = {
        "target_url": args.target_url or file_input.get("site", {}).get("url", None),
        "target_name": args.target_name or file_input.get("site", {}).get("name", None),
        "target_type": get_target_type(args, file_input),
        "api_schema_type": get_api_schema_type(args, file_input),
        "api_schema_file_url": args.api_schema_file_url
        or file_input.get("site", {})
        .get("api_scan_settings", {})
        .get("api_schema_url", None),
        "file_input": file_input,
    }

    return command_arguments


def targets_add_command_handler(args: argparse.Namespace):
    command_arguments = get_command_arguments(args)

    if not command_arguments["target_url"]:
        raise ProbelyCLIValidation("must provide a target URL by argument or yaml-file")

    api_scan_settings = validate_and_retrieve_api_scan_settings(
        target_type=command_arguments.get("target_type"),
        api_schema_file_url=command_arguments.get("api_schema_file_url"),
        api_schema_type=command_arguments.get("api_schema_type"),
    )

    logger.debug("target add extra_payload: {}".format(command_arguments["file_input"]))

    target: dict = add_target(
        target_url=command_arguments["target_url"],
        target_name=command_arguments["target_name"],
        target_type=command_arguments["target_type"],
        api_schema_file_url=api_scan_settings.get("api_schema_file_url", None),
        api_schema_type=api_scan_settings.get("api_schema_type", None),
        extra_payload=command_arguments["file_input"],
    )

    cmd_output = build_cmd_output(args, target)
    args.console.print(cmd_output)
