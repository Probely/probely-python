import argparse

from rich_argparse import RichHelpFormatter

from probely.cli.commands.findings.get import findings_get_command_handler
from probely.cli.parsers.common import (
    build_configs_parser,
    build_output_parser,
    ProbelyArgumentParser,
    show_help,
)
from probely.cli.parsers.help_texts import (
    SUB_COMMAND_AVAILABLE_ACTIONS_TITLE,
    FINDINGS_F_SEARCH_TEXT,
    FINDINGS_GET_COMMAND_DESCRIPTION_TEXT,
    FINDINGS_COMMAND_DESCRIPTION_TEXT,
)
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
        metavar="SEARCH_TERM",
        help=FINDINGS_F_SEARCH_TEXT,
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


def build_findings_parser():
    findings_filter_parser = build_findings_filters_parser()
    configs_parser = build_configs_parser()
    output_parser = build_output_parser()

    findings_parser = ProbelyArgumentParser(
        prog="probely findings",
        add_help=False,
        description=FINDINGS_COMMAND_DESCRIPTION_TEXT,
    )
    findings_parser.set_defaults(
        command_handler=show_help,
        is_no_action_parser=True,
        parser=findings_parser,
    )

    findings_command_parser = findings_parser.add_subparsers(
        title=SUB_COMMAND_AVAILABLE_ACTIONS_TITLE,
    )

    findings_get_parser = findings_command_parser.add_parser(
        "get",
        help=FINDINGS_GET_COMMAND_DESCRIPTION_TEXT,
        parents=[configs_parser, findings_filter_parser, output_parser],
    )

    findings_get_parser.add_argument(
        "findings_ids",
        metavar="FINDING_ID",
        nargs="*",
        help="Identifiers of the findings to list",
    )

    findings_get_parser.set_defaults(
        command_handler=findings_get_command_handler,
        parser=findings_get_parser,
    )

    return findings_parser
