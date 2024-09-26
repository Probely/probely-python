import argparse

from probely_cli.cli.commands.scans.schemas import ScanApiFiltersSchema
from probely_cli.cli.common import prepare_filters_for_api
from probely_cli.cli.enums import EntityTypeEnum, OutputEnum
from probely_cli.cli.renderers import OutputRenderer
from probely_cli.exceptions import ProbelyCLIValidation
from probely_cli.sdk.scans import list_scans, retrieve_scans


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
        entity_type=EntityTypeEnum.SCAN,
    )
    renderer.render()
