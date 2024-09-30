import json
import logging
import sys
from typing import Dict, List

import yaml

from probely.cli.commands.targets.schemas import TargetApiFiltersSchema
from probely.cli.common import (
    prepare_filters_for_api,
    validate_and_retrieve_yaml_content,
)
from probely.cli.enums import OutputEnum
from probely.exceptions import ProbelyCLIValidation
from probely.sdk.targets import list_targets, update_target, update_targets

logger = logging.getLogger(__name__)


def display_cmd_output(args, updated_targets: List[Dict]):
    """
    If the --output arg is provided, display targets' data in the specified format (JSON/YAML).
    Otherwise, display only the Target IDs line by line.
    """
    output_type = OutputEnum[args.output] if args.output else None

    if not output_type:
        for target in updated_targets:
            args.console.print(target["id"])
        return

    if output_type == OutputEnum.JSON:
        output = json.dumps(updated_targets, indent=2)
    else:
        output = yaml.dump(updated_targets, indent=2, width=sys.maxsize)

    args.console.print(output)


def update_targets_command_handler(args):
    """
    Update targets based on the provided filters or target IDs.
    """
    yaml_file_path = args.yaml_file_path
    if not yaml_file_path:
        raise ProbelyCLIValidation(
            "Path to the YAML file that contains the payload is required."
        )
    payload = validate_and_retrieve_yaml_content(yaml_file_path)

    filters = prepare_filters_for_api(TargetApiFiltersSchema, args)
    targets_ids = args.target_ids

    if not filters and not targets_ids:
        raise ProbelyCLIValidation("either filters or Target IDs must be provided.")

    if filters and targets_ids:
        raise ProbelyCLIValidation("filters and Target IDs are mutually exclusive.")

    logger.debug("Payload for targets update: %s", payload)

    if targets_ids:
        if len(targets_ids) == 1:
            updated_targets = [update_target(targets_ids[0], payload)]
        else:
            updated_targets = update_targets(targets_ids, payload)
        display_cmd_output(args, updated_targets)
        return

    # Fetch all Targets that match the filters and update them
    generator = list_targets(targets_filters=filters)
    first_target = next(generator, None)

    if not first_target:
        raise ProbelyCLIValidation("Selected Filters returned no results")

    targets_ids = [first_target["id"]] + [target["id"] for target in generator]

    if len(targets_ids) == 1:
        updated_targets = [update_target(targets_ids[0], payload)]
    else:
        updated_targets = update_targets(targets_ids, payload)
    display_cmd_output(args, updated_targets)
