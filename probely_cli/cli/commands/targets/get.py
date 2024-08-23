from typing import List, Dict, Union

import marshmallow
from dateutil import parser
from marshmallow import Schema
from rich.table import Table

from probely_cli.cli.commands.targets.schemas import TargetApiFiltersSchema
from probely_cli.cli.common import TargetRiskEnum
from probely_cli.exceptions import ProbelyCLIValidation
from probely_cli.sdk.targets import list_targets, retrieve_targets

TARGET_NEVER_SCANNED_OUTPUT: str = "Never scanned"


def _get_printable_last_scan_date(target: Dict) -> str:
    last_scan_obj: Union[dict, None] = target.get("last_scan", None)

    if last_scan_obj is None:
        return TARGET_NEVER_SCANNED_OUTPUT

    last_scan_start_date_str: Union[str, None] = last_scan_obj.get("started", None)

    if last_scan_start_date_str is None:
        return TARGET_NEVER_SCANNED_OUTPUT

    last_start_date = parser.isoparse(last_scan_start_date_str)
    return last_start_date.strftime("%Y-%m-%d %H:%m")


def _get_printable_risk(target: Dict) -> str:
    target_risk_value = target.get("risk", None)
    try:
        risk_name: str = TargetRiskEnum.get_by_api_response_value(
            target_risk_value
        ).name
        return risk_name
    except ValueError:
        return "Unknown"  # TODO: scenario that risk enum updated but CLI is forgotten


def _get_printable_labels(target: Dict) -> str:
    labels: List[Dict] = target.get("labels", [])
    labels_name = []
    try:
        [labels_name.append(label["name"]) for label in labels]
    except:
        return "Unknown labels"

    printable_labels = ", ".join(labels_name)

    return printable_labels


def get_tabled_targets(targets_list: List[Dict]):
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
            _get_printable_risk(target),
            _get_printable_last_scan_date(target),
            _get_printable_labels(target),
        )

    return table


def target_filters_handler(args):
    filters_schema: Schema = TargetApiFiltersSchema()
    try:
        api_ready_filters = filters_schema.load(vars(args))
    except marshmallow.ValidationError as e:
        # TODO: translate validations?
        raise ProbelyCLIValidation(str(e))

    return api_ready_filters


def targets_get_command_handler(args):
    """
    Lists all accessible targets of client
    """

    filters = target_filters_handler(args)
    if filters and args.target_ids:
        raise ProbelyCLIValidation("filters and target ids are mutually exclusive.")

    if args.target_ids:
        targets_list = retrieve_targets(args.target_ids)
    else:
        targets_list = list_targets(targets_filters=filters)

    table = get_tabled_targets(targets_list)
    args.console.print(table)
