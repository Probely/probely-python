import argparse

from rich_argparse import RichHelpFormatter

from probely_cli.cli.commands.findings.get import findings_get_command_handler
from probely_cli.cli.common import (
    show_help,
    FindingSeverityEnum,
    lowercase_acceptable_parser_type,
    FindingStateEnum,
)
from probely_cli.settings import TRUTHY_VALUES, FALSY_VALUES


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
        type=lowercase_acceptable_parser_type,
        nargs="+",
        choices=FindingSeverityEnum.cli_input_choices(),
        help="Filter findings by list of severities",
        action="store",
    )

    findings_filters_parser.add_argument(
        "--f-state",
        type=lowercase_acceptable_parser_type,
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
        type=lowercase_acceptable_parser_type,
        choices=TRUTHY_VALUES + FALSY_VALUES,
        help="Filter new findings",
        action="store",
    )

    return findings_filters_parser


def build_findings_parser(commands_parser, configs_parser):
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
        parents=[configs_parser, findings_filter_parser],
        formatter_class=RichHelpFormatter,
    )

    findings_get_parser.set_defaults(
        command_handler=findings_get_command_handler,
        parser=findings_get_parser,
    )
