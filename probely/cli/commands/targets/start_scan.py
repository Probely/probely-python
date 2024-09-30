import logging

from probely.cli.commands.targets.schemas import TargetApiFiltersSchema
from probely.cli.common import (
    display_scans_response_output,
    prepare_filters_for_api,
    validate_and_retrieve_yaml_content,
)
from probely.exceptions import ProbelyCLIValidation
from probely.sdk.scans import start_scan, start_scans
from probely.sdk.targets import list_targets

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
    filters = prepare_filters_for_api(TargetApiFiltersSchema, args)
    targets_ids = args.target_ids

    if not filters and not targets_ids:
        raise ProbelyCLIValidation("either filters or Target IDs must be provided.")

    if filters and targets_ids:
        raise ProbelyCLIValidation("filters and Target IDs are mutually exclusive.")

    extra_payload = validate_and_retrieve_extra_payload(args)

    if filters:
        generator = list_targets(targets_filters=filters)
        first_target = next(generator, None)

        if not first_target:
            raise ProbelyCLIValidation("Selected Filters returned no results")

        targets_ids = [first_target["id"]] + [target["id"] for target in generator]

    if len(targets_ids) == 1:
        scans = [start_scan(targets_ids[0], extra_payload)]
    else:
        scans = start_scans(targets_ids, extra_payload)

    display_scans_response_output(args, scans)
