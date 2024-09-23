import json
import sys
from typing import Dict, Generator, Optional

import marshmallow
import yaml
from marshmallow import Schema
from rich.console import Console
from rich.live import Live
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


def finding_filters_handler(args):
    filters_schema: Schema = FindingsApiFiltersSchema()
    try:
        api_ready_filters = filters_schema.load(vars(args))
    except marshmallow.ValidationError as e:
        raise ProbelyCLIValidation(str(e))

    return api_ready_filters


def create_findings_table(show_header: bool = False) -> Table:
    """
    Initializes and returns a Rich Table for displaying Findings.
    """
    table = Table(show_header=show_header, box=None)

    table.add_column("ID", width=18)
    table.add_column("TARGET_ID", width=12)
    table.add_column("SEVERITY", width=8)
    table.add_column("TITLE", width=48, no_wrap=True)
    table.add_column("LAST_FOUND", width=16)
    table.add_column("STATE", width=8)
    table.add_column("LABELS", width=16)

    return table


def add_finding_to_table(table: Table, finding: Dict) -> None:
    """
    Adds a single finding as a row to the provided Rich Table.
    """
    target = finding.get("target")

    table.add_row(
        f"{target['id']}-{finding['id']}",  # Composite Finding ID
        target["id"],  # target_id
        get_printable_enum_value(FindingSeverityEnum, finding["severity"]),  # severity
        finding["definition"]["name"],  # title
        get_printable_date(
            finding["last_found"], DEFAULT_LAST_FOUND_DATE_VALUE
        ),  # last_found
        finding["state"],  # state
        get_printable_labels(finding["labels"]),  # labels
    )


def render_json_output(findings: Generator[Dict, None, None], console: Console) -> None:
    console.print("[")
    first = True
    for finding in findings:
        if not first:
            console.print(",")
        console.print(json.dumps(finding, indent=2))
        first = False
    console.print("]")


def render_yaml_output(findings: Generator[Dict, None, None], console: Console) -> None:
    for finding in findings:
        console.print(yaml.dump([finding], indent=2, width=sys.maxsize))


def render_table_output(
    findings: Generator[Dict, None, None], console: Console
) -> None:
    table = create_findings_table(show_header=True)
    with Live(table, refresh_per_second=1, console=console):
        for finding in findings:
            add_finding_to_table(table, finding)


def render_output(
    findings: Generator[Dict, None, None],
    output_type: Optional[OutputEnum],
    console: Console,
) -> None:
    if output_type == OutputEnum.JSON:
        render_json_output(findings, console)
    elif output_type == OutputEnum.YAML:
        render_yaml_output(findings, console)
    else:
        render_table_output(findings, console)


def findings_get_command_handler(args):
    api_filters = finding_filters_handler(args)
    if api_filters and args.findings_ids:
        raise ProbelyCLIValidation("filters and finding ids are mutually exclusive.")

    if args.findings_ids:
        findings_generator = retrieve_findings(findings_ids=args.findings_ids)
    else:
        findings_generator = list_findings(findings_filters=api_filters)

    output_type = OutputEnum[args.output] if args.output else None
    render_output(findings_generator, output_type, args.console)
