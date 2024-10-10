import argparse

from probely.cli.commands.findings.schemas import FindingsApiFiltersSchema
from probely.cli.common import prepare_filters_for_api
from probely.cli.enums import OutputEnum
from probely.cli.renderers import OutputRenderer
from probely.cli.tables.finding_table import FindingTable
from probely.exceptions import ProbelyCLIValidation
from probely.sdk.findings import list_findings, retrieve_findings


def findings_get_command_handler(args: argparse.Namespace):
    filters = prepare_filters_for_api(FindingsApiFiltersSchema, args)
    if filters and args.findings_ids:
        raise ProbelyCLIValidation("filters and Finding IDs are mutually exclusive.")

    if args.findings_ids:
        findings_generator = retrieve_findings(findings_ids=args.findings_ids)
    else:
        findings_generator = list_findings(findings_filters=filters)

    output_type = OutputEnum[args.output] if args.output else None
    renderer = OutputRenderer(
        records=findings_generator,
        output_type=output_type,
        console=args.console,
        table_cls=FindingTable,
    )
    renderer.render()
