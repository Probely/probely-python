import argparse
import json
import sys
from typing import Dict, List

import marshmallow
import yaml

from probely_cli.cli.commands.scans.schemas import ScanApiFiltersSchema
from probely_cli.cli.common import OutputEnum
from probely_cli.cli.formatters import get_printable_date, get_printable_labels
from probely_cli.exceptions import ProbelyCLIValidation
from probely_cli.sdk.scans import list_scans, retrieve_scans
from rich.table import Table


def get_tabled_scans(scans: list) -> Table:
    table = Table(box=None)
    table.add_column("ID")
    table.add_column("NAME")
    table.add_column("URL")
    table.add_column("STATUS")
    table.add_column("START_DATE")
    table.add_column("HIGH_RISKS")
    table.add_column("MEDIUM_RISKS")
    table.add_column("LOW_RISKS")
    table.add_column("LABELS")

    for scan in scans:
        target = scan.get("target")
        site = target.get("site")

        table.add_row(
            scan.get("id"),
            site.get("name", "N/D"),
            site.get("url"),
            scan["status"],
            get_printable_date(scan["started"]),
            str(scan["highs"]),
            str(scan["mediums"]),
            str(scan["lows"]),
            get_printable_labels(target["labels"]),
        )

    return table


def prepare_scan_filters_for_api(args: argparse.Namespace) -> dict:
    filters_schema: marshmallow.Schema = ScanApiFiltersSchema()
    try:
        filters = filters_schema.load(vars(args))
    except marshmallow.ValidationError as ex:
        raise ProbelyCLIValidation("Invalid filters: {}".format(ex))

    return filters


def build_cmd_output(args, scans: List[Dict]) -> Table:
    output_type = OutputEnum[args.output] if args.output else None

    if output_type == OutputEnum.JSON:
        return json.dumps(scans, indent=2)

    if output_type == OutputEnum.YAML:
        return yaml.dump(
            scans,
            indent=2,
            width=sys.maxsize,
        )

    return get_tabled_scans(scans)


def scans_get_command_handler(args: argparse.Namespace):
    filters = prepare_scan_filters_for_api(args)
    if filters and args.scan_ids:
        raise ProbelyCLIValidation("Filters and Scan IDs are mutually exclusive")

    if args.scan_ids:
        scans_list = retrieve_scans(args.scan_ids)
    else:
        scans_list = list_scans(scans_filters=filters)

    cmd_output = build_cmd_output(args, scans_list)
    args.console.print(cmd_output)
