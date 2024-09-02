from probely_cli.cli.commands.targets.get import (
    target_filters_handler,
)
from probely_cli.exceptions import ProbelyCLIValidation
from probely_cli.sdk.targets import delete_targets, list_targets


def targets_delete_command_handler(args):
    """
    Delete targets
    """

    filters = target_filters_handler(args)

    if not filters and not args.target_ids:
        args.parser.print_help()
        return

    if filters and args.target_ids:
        raise ProbelyCLIValidation("filters and target ids are mutually exclusive.")

    targets_list_ids = args.target_ids

    if not args.target_ids:
        targets_list = list_targets(targets_filters=filters)
        targets_list_ids = [target.get("id") for target in targets_list]

    targets = delete_targets(targets_ids=targets_list_ids)
    for ids in targets.get("ids"):
        args.console.print(ids)
