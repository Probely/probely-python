import argparse

from rich_argparse import RichHelpFormatter

from probely.cli.commands.findings.get import findings_get_command_handler
from probely.cli.common import show_help
from probely.sdk.enums import FindingSeverityEnum, FindingStateEnum
from probely.settings import FALSY_VALUES, TRUTHY_VALUES


def build_findings_filters_parser() -> argparse.ArgumentParser:
    findings_filters_parser = argparse.ArgumentParser(
        description="Filters usable in Targets commands",
        add_help=False,
        formatter_class=RichHelpFormatter,
    )

    findings_filters_parser.add_argument(
        "--f-scans",
        nargs="+",
        help="Filter findings by list of origin scans",
        action="store",
    )

    findings_filters_parser.add_argument(
        "--f-severity",
        type=str.upper,
        nargs="+",
        choices=FindingSeverityEnum.cli_input_choices(),
        help="Filter findings by list of severities",
        action="store",
    )

    findings_filters_parser.add_argument(
        "--f-state",
        type=str.upper,
        nargs="+",
        choices=FindingStateEnum.cli_input_choices(),
        help="Filter findings by list of states",
        action="store",
    )

    findings_filters_parser.add_argument(
        "--f-targets",
        nargs="+",
        help="Filter findings by list of origin targets",
        action="store",
    )

    findings_filters_parser.add_argument(
        "--f-search",
        help="Filter findings by keyword",
        action="store",
    )

    findings_filters_parser.add_argument(
        "--f-is-new",
        type=str.upper,
        choices=TRUTHY_VALUES + FALSY_VALUES,
        help="Filter new findings",
        action="store",
    )

    return findings_filters_parser


def build_findings_parser(commands_parser, configs_parser, output_parser):
    findings_filter_parser = build_findings_filters_parser()

    findings_parser = commands_parser.add_parser(
        "findings",
        parents=[configs_parser],
        formatter_class=RichHelpFormatter,
    )
    findings_parser.set_defaults(
        command_handler=show_help,
        is_no_action_parser=True,
        parser=findings_parser,
        formatter_class=RichHelpFormatter,
    )

    findings_command_parser = findings_parser.add_subparsers()

    findings_get_parser = findings_command_parser.add_parser(
        "get",
        help="Lists all findings",
        parents=[configs_parser, findings_filter_parser, output_parser],
        formatter_class=RichHelpFormatter,
    )

    findings_get_parser.add_argument(
        "findings_ids",
        metavar="FINDING_ID",
        nargs="*",
        help="IDs of findings to list",
    )

    findings_get_parser.set_defaults(
        command_handler=findings_get_command_handler,
        parser=findings_get_parser,
    )
