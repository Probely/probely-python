from typing import Dict, List

import marshmallow
from marshmallow import Schema
from rich.table import Table

from probely_cli.cli.commands.findings.schemas import FindingsApiFiltersSchema
from probely_cli.cli.common import (
    FindingSeverityEnum,
)
from probely_cli.cli.formatters import get_printable_enum_value, get_printable_date, \
    get_printable_labels
from probely_cli.exceptions import ProbelyCLIValidation
from probely_cli.sdk.findings import list_findings

DEFAULT_LAST_FOUND_DATE_VALUE = "NO_DATE"


def get_tabled_findings(findings_list: List[Dict]):
    table = Table(box=None)
    table.add_column("ID")
    table.add_column("TARGET_ID")
    table.add_column("SEVERITY")
    table.add_column("TITLE")
    table.add_column("LAST_FOUND")
    table.add_column("STATE")
    table.add_column("LABELS")

    for finding in findings_list:
        target = finding.get("target")

        table.add_row(
            str(finding["id"]),  # id
            target["id"],  # target_id
            get_printable_enum_value(FindingSeverityEnum, finding["severity"]),
            finding["definition"]["name"],  # title
            get_printable_date(
                finding["last_found"],
                DEFAULT_LAST_FOUND_DATE_VALUE,  # last_found
            ),
            finding["state"],  # state
            get_printable_labels(finding["labels"]),  # labels
        )
    return table


def finding_filters_handler(args):
    filters_schema: Schema = FindingsApiFiltersSchema()
    try:
        api_ready_filters = filters_schema.load(vars(args))
    except marshmallow.ValidationError as e:
        # TODO: translate validations?
        raise ProbelyCLIValidation(str(e))

    return api_ready_filters


def findings_get_command_handler(args):

    api_filters = finding_filters_handler(args)

    findings_list = list_findings(findings_filters=api_filters)

    findings_output = get_tabled_findings(findings_list)
    args.console.print(findings_output)
