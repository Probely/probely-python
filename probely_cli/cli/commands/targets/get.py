import json
import sys
from typing import List, Dict, Union

import marshmallow
import yaml
from marshmallow import Schema
from rich.table import Table

from probely_cli.cli.commands.targets.schemas import TargetApiFiltersSchema
from probely_cli.cli.common import OutputEnum, TargetRiskEnum
from probely_cli.cli.formatters import (
    get_printable_date,
    get_printable_enum_value,
    get_printable_labels,
)
from probely_cli.exceptions import ProbelyCLIValidation
from probely_cli.sdk.targets import list_targets, retrieve_targets

TARGET_NEVER_SCANNED_OUTPUT: str = "Never_scanned"


def _get_printable_last_scan_date(target: Dict) -> str:
    last_scan_obj: Union[dict, None] = target.get("last_scan", None)

    if last_scan_obj is None:
        return TARGET_NEVER_SCANNED_OUTPUT

    last_scan_start_date_str: Union[str, None] = last_scan_obj.get("started", None)

    return get_printable_date(last_scan_start_date_str, TARGET_NEVER_SCANNED_OUTPUT)


def get_tabled_targets(targets_list: List[Dict]) -> Table:
    table = Table(box=None)
    table.add_column("ID")
    table.add_column("NAME")
    table.add_column("URL")
    table.add_column("RISK")
    table.add_column("LAST_SCAN")
    table.add_column("LABELS")

    for target in targets_list:
        asset = target.get("site")

        table.add_row(
            target.get("id"),
            asset.get("name", "N/D"),
            asset.get("url"),
            get_printable_enum_value(TargetRiskEnum, target["risk"]),
            _get_printable_last_scan_date(target),  # last_scan
            get_printable_labels(target["labels"]),
        )

    return table


def target_filters_handler(args) -> dict:
    filters_schema: Schema = TargetApiFiltersSchema()
    try:
        api_ready_filters = filters_schema.load(vars(args))
    except marshmallow.ValidationError as e:
        # TODO: translate validations?
        raise ProbelyCLIValidation(str(e))

    return api_ready_filters


def build_cmd_output(args, targets_list):
    output_type = OutputEnum[args.output] if args.output else None

    if output_type == OutputEnum.JSON:
        return json.dumps(targets_list, indent=2)

    if output_type == OutputEnum.YAML:
        return yaml.dump(
            targets_list,
            indent=2,
            width=sys.maxsize,  # avoids word wrapping
        )

    return get_tabled_targets(targets_list)


def targets_get_command_handler(args):
    """
    Lists all accessible targets of client
    """
    filters = target_filters_handler(args)
    targets_ids = args.target_ids

    if filters and targets_ids:
        raise ProbelyCLIValidation("filters and Target IDs are mutually exclusive.")

    if targets_ids:
        targets_list = retrieve_targets(targets_ids=targets_ids)
    else:
        targets_list = list_targets(targets_filters=filters)

    cmd_output = build_cmd_output(args, targets_list)
    args.console.print(cmd_output)
