import logging

from probely_cli.cli.commands.targets.get import target_filters_handler
from probely_cli.cli.common import (
    display_scans_response_output,
    validate_and_retrieve_yaml_content,
)
from probely_cli.exceptions import ProbelyCLIValidation
from probely_cli.sdk.scans import start_scan, start_scans
from probely_cli.sdk.targets import list_targets

logger = logging.getLogger(__name__)

def validate_and_retrieve_extra_payload(args):
    extra_payload = validate_and_retrieve_yaml_content(args.yaml_file_path)

    if "targets" in extra_payload:
        #  NOTE: This is only for alpha version, specifying Target IDs in the file will be supported in the future
        raise ProbelyCLIValidation(
            "Target IDs should be provided only through CLI, not in the YAML file."
        )

    return extra_payload


def start_scans_command_handler(args):
    filters = target_filters_handler(args)
    targets_ids = args.target_ids

    if not filters and not targets_ids:
        raise ProbelyCLIValidation("either filters or Target IDs must be provided.")

    if filters and targets_ids:
        raise ProbelyCLIValidation("filters and Target IDs are mutually exclusive.")

    extra_payload = validate_and_retrieve_extra_payload(args)

    if filters:
        searched_targets = list_targets(targets_filters=filters)

        if not searched_targets:
            raise ProbelyCLIValidation("Selected Filters returned no results")

        targets_ids = [target["id"] for target in searched_targets]

    if len(targets_ids) == 1:
        scans = [start_scan(targets_ids[0], extra_payload)]
    else:
        scans = start_scans(targets_ids, extra_payload)
    display_scans_response_output(args, scans)
