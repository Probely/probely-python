from probely.cli.commands.targets.schemas import TargetApiFiltersSchema
from probely.cli.common import prepare_filters_for_api
from probely.exceptions import ProbelyCLIValidation
from probely.sdk.targets import delete_target, delete_targets, list_targets


def targets_delete_command_handler(args):
    """
    Delete targets
    """
    filters = prepare_filters_for_api(TargetApiFiltersSchema, args)
    targets_ids = args.target_ids

    if not filters and not targets_ids:
        raise ProbelyCLIValidation("Expected target_ids or filters")

    if filters and targets_ids:
        raise ProbelyCLIValidation("filters and Target IDs are mutually exclusive.")

    if filters:
        generator = list_targets(targets_filters=filters)
        first_target = next(generator, None)

        if not first_target:
            raise ProbelyCLIValidation("Selected Filters returned no results")

        targets_ids = [first_target.get("id")] + [
            target.get("id") for target in generator
        ]

    if len(targets_ids) == 1:
        target_id = delete_target(targets_ids[0])
        args.console.print(target_id)
        return

    targets = delete_targets(targets_ids=targets_ids)

    for ids in targets.get("ids"):
        args.console.print(ids)
