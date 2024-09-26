from probely_cli.cli.commands.targets.get import target_filters_handler
from probely_cli.exceptions import ProbelyCLIValidation
from probely_cli.sdk.targets import delete_target, delete_targets, list_targets


def targets_delete_command_handler(args):
    """
    Delete targets
    """
    filters = target_filters_handler(args)
    targets_ids = args.target_ids

    if not filters and not targets_ids:
        raise ProbelyCLIValidation("Expected target_ids or filters")

    if filters and targets_ids:
        raise ProbelyCLIValidation("filters and Target IDs are mutually exclusive.")

    if filters:
        targets_list = list_targets(targets_filters=filters)
        targets_ids = [target.get("id") for target in targets_list]

    if len(targets_ids) == 1:
        target_id = delete_target(targets_ids[0])
        args.console.print(target_id)
        return

    targets = delete_targets(targets_ids=targets_ids)

    for ids in targets.get("ids"):
        args.console.print(ids)
