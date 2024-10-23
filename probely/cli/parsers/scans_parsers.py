import argparse

from probely.cli.commands.scans.cancel import scans_cancel_command_handler
from probely.cli.commands.scans.get import scans_get_command_handler
from probely.cli.commands.scans.pause import scans_pause_command_handler
from probely.cli.commands.scans.resume import scans_resume_command_handler
from probely.cli.parsers.common import (
    build_configs_parser,
    build_output_parser,
    ProbelyArgumentParser,
    show_help,
)
from probely.cli.parsers.help_texts import (
    SCANS_PAUSE_COMMAND_DESCRIPTION_TEXT,
    SCANS_CANCEL_COMMAND_DESCRIPTION_TEXT,
    SCANS_RESUME_COMMAND_DESCRIPTION_TEXT,
    SCANS_GET_COMMAND_DESCRIPTION_TEXT,
    SUB_COMMAND_AVAILABLE_ACTIONS_TITLE,
    SCANS_F_SEARCH_TEXT,
    SCANS_COMMAND_DESCRIPTION_TEXT,
)
from probely.sdk.enums import ScanStatusEnum


def build_scan_filters_parser() -> argparse.ArgumentParser:
    scan_filters_parser = ProbelyArgumentParser(
        add_help=False,
        description=SCANS_COMMAND_DESCRIPTION_TEXT,
    )

    scan_filters_parser.add_argument(
        "--f-search",
        metavar="SEARCH_TERM",
        action="store",
        default=None,
        help=SCANS_F_SEARCH_TEXT,
    )

    scan_filters_parser.add_argument(
        "--f-status",
        action="store",
        nargs="+",
        type=str.upper,
        choices=ScanStatusEnum.cli_input_choices(),
        help="Filter by Scan status",
    )

    date_filters_group = scan_filters_parser.add_argument_group(
        "Date Filters",
        "Specify the date or datetime for filtering Scans. Use the ISO 8601 format, "
        "for example: `2020-07-05` for a date, or `2020-07-05T12:45:30` for a datetime.",
    )
    for date_field in ["completed", "started"]:
        for filter_lookup, description in {
            "gt": "after",
            "gte": "on or after",
            "lt": "before",
            "lte": "on or before",
        }.items():
            date_filters_group.add_argument(
                f"--f-{date_field}-{filter_lookup}",
                action="store",
                default=None,
                metavar="DATETIME",
                help=(
                    f"Filter scans {date_field} {description} the specified date or datetime."
                ),
            )
    return scan_filters_parser


def build_scans_parser():
    scan_filters_parser = build_scan_filters_parser()

    configs_parser = build_configs_parser()
    output_parser = build_output_parser()

    scans_parser = ProbelyArgumentParser(
        prog="probely scans",
        add_help=False,
        description="Manage existing scans",
    )
    scans_parser.set_defaults(
        command_handler=show_help,
        is_no_action_parser=True,
        parser=scans_parser,
    )

    scans_command_parser = scans_parser.add_subparsers(
        title=SUB_COMMAND_AVAILABLE_ACTIONS_TITLE,
    )

    scans_get_parser = scans_command_parser.add_parser(
        "get",
        help=SCANS_GET_COMMAND_DESCRIPTION_TEXT,
        parents=[configs_parser, scan_filters_parser, output_parser],
    )
    scans_get_parser.add_argument(
        "scan_ids",
        metavar="SCAN_ID",
        nargs="*",
        help="Identifiers of the scans to list",
        default=None,
    )
    scans_get_parser.set_defaults(
        command_handler=scans_get_command_handler,
        parser=scans_get_parser,
    )

    scans_pause_parser = scans_command_parser.add_parser(
        "pause",
        help=SCANS_PAUSE_COMMAND_DESCRIPTION_TEXT,
        parents=[configs_parser, scan_filters_parser, output_parser],
    )
    scans_pause_parser.add_argument(
        "scan_ids",
        metavar="SCAN_ID",
        nargs="*",
        help="Identifiers of the scans to pause.",
        default=None,
    )
    scans_pause_parser.set_defaults(
        command_handler=scans_pause_command_handler,
        parser=scans_pause_parser,
    )

    scans_cancel_parser = scans_command_parser.add_parser(
        "cancel",
        help=SCANS_CANCEL_COMMAND_DESCRIPTION_TEXT,
        parents=[configs_parser, scan_filters_parser, output_parser],
    )
    scans_cancel_parser.add_argument(
        "scan_ids",
        metavar="SCAN_ID",
        nargs="*",
        help="Identifiers of the scans to cancel",
        default=None,
    )
    scans_cancel_parser.set_defaults(
        command_handler=scans_cancel_command_handler,
        parser=scans_cancel_parser,
    )

    scans_resume_parser = scans_command_parser.add_parser(
        "resume",
        help=SCANS_RESUME_COMMAND_DESCRIPTION_TEXT,
        parents=[configs_parser, scan_filters_parser, output_parser],
    )
    scans_resume_parser.add_argument(
        "scan_ids",
        metavar="SCAN_ID",
        nargs="*",
        help="Identifiers of the scans to resume",
        default=None,
    )
    scans_resume_parser.add_argument(
        "--ignore-blackout-period",
        help="Ignore blackout period settings",
        action="store_true",
    )
    scans_resume_parser.set_defaults(
        command_handler=scans_resume_command_handler,
        parser=scans_resume_parser,
    )

    return scans_parser
