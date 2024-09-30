import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Type, Union

import marshmallow
import yaml

import probely.settings as settings
from probely.cli.enums import OutputEnum
from probely.exceptions import ProbelyCLIValidation


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


def display_scans_response_output(args, scans: List[Dict]):
    """
    If the --output arg is provided, display Scans' data in the specified format (JSON/YAML).
    Otherwise, display only the Scan IDs line by line.
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


def prepare_filters_for_api(
    schema: Type[marshmallow.Schema], args: argparse.Namespace
) -> dict:
    """
    Prepares and validates filters using the provided Marshmallow schema.
    """
    filters_schema = schema()
    try:
        filters = filters_schema.load(vars(args))
    except marshmallow.ValidationError as ex:
        raise ProbelyCLIValidation(f"Invalid filters: {ex}")
    return filters
