import argparse

from probely.cli.commands.scans.schemas import ScanApiFiltersSchema
from probely.cli.common import prepare_filters_for_api
from probely.cli.enums import OutputEnum
from probely.cli.renderers import OutputRenderer
from probely.cli.tables.scan_table import ScanTable
from probely.exceptions import ProbelyCLIValidation
from probely.sdk.scans import list_scans, retrieve_scans


def scans_get_command_handler(args: argparse.Namespace):
    filters = prepare_filters_for_api(ScanApiFiltersSchema, args)
    scan_ids = args.scan_ids

    if filters and scan_ids:
        raise ProbelyCLIValidation("filters and Scan IDs are mutually exclusive.")

    if scan_ids:
        scans_generator = retrieve_scans(scan_ids=args.scan_ids)
    else:
        scans_generator = list_scans(scans_filters=filters)

    output_type = OutputEnum[args.output] if args.output else None
    renderer = OutputRenderer(
        records=scans_generator,
        output_type=output_type,
        console=args.console,
        table_cls=ScanTable,
    )
    renderer.render()
