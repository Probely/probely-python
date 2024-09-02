import json
import sys
from typing import Dict, List

import marshmallow
import yaml
from marshmallow import Schema
from rich.table import Table

from probely_cli.cli.commands.findings.schemas import FindingsApiFiltersSchema
from probely_cli.cli.common import (
    FindingSeverityEnum,
    OutputEnum,
)
from probely_cli.cli.formatters import (
    get_printable_enum_value,
    get_printable_date,
    get_printable_labels,
)
from probely_cli.exceptions import ProbelyCLIValidation
from probely_cli.sdk.findings import list_findings
from probely_cli.sdk.findings import retrieve_findings

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
            "{target_id}-{finding_id}".format(
                target_id=str(target["id"]), finding_id=str(finding["id"])
            ),  # id
            target["id"],
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

    return get_tabled_findings(targets_list)


def findings_get_command_handler(args):
    api_filters = finding_filters_handler(args)
    if api_filters and args.findings_ids:
        raise ProbelyCLIValidation("filters and finding ids are mutually exclusive.")

    if args.findings_ids:
        findings_list = retrieve_findings(findings_ids=args.findings_ids)
    else:
        findings_list = list_findings(findings_filters=api_filters)

    findings_output = build_cmd_output(args, findings_list)
    args.console.print(findings_output)
