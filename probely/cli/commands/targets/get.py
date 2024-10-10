from probely.cli.commands.targets.schemas import TargetApiFiltersSchema
from probely.cli.common import prepare_filters_for_api
from probely.cli.enums import OutputEnum

from probely.cli.renderers import OutputRenderer
from probely.cli.tables.targets_table import TargetTable
from probely.exceptions import ProbelyCLIValidation
from probely.sdk.targets import list_targets, retrieve_targets


def targets_get_command_handler(args):
    """
    Lists all accessible targets of client
    """
    filters = prepare_filters_for_api(TargetApiFiltersSchema, args)
    targets_ids = args.target_ids

    if filters and targets_ids:
        raise ProbelyCLIValidation("filters and Target IDs are mutually exclusive.")

    if targets_ids:
        targets_generator = retrieve_targets(targets_ids=targets_ids)
    else:
        targets_generator = list_targets(targets_filters=filters)

    output_type = OutputEnum[args.output] if args.output else None

    renderer = OutputRenderer(
        records=targets_generator,
        output_type=output_type,
        console=args.console,
        table_cls=TargetTable,
    )
    renderer.render()
