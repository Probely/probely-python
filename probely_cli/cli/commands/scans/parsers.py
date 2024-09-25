import argparse

from rich_argparse import RichHelpFormatter

from probely_cli.cli.commands.scans.cancel import scans_cancel_command_handler
from probely_cli.cli.commands.scans.get import scans_get_command_handler
from probely_cli.cli.commands.scans.pause import scans_pause_command_handler
from probely_cli.cli.commands.scans.resume import scans_resume_command_handler
from probely_cli.cli.common import show_help
from probely_cli.sdk.common import ScanStatusEnum


def build_scan_filters_parser() -> argparse.ArgumentParser:
    scan_filters_parser = argparse.ArgumentParser(
        description="Filters usable in Scan commands",
        add_help=False,
        formatter_class=RichHelpFormatter,
    )
    scan_filters_parser.add_argument(
        "--f-search",
        action="store",
        default=None,
        metavar="SEARCH TERM",
        help="Keyword to match with Scan URL, Target name, URL or labels",
    )

    scan_filters_parser.add_argument(
        "--f-status",
        action="store",
        nargs="+",
        type=str.upper,
        choices=ScanStatusEnum.cli_input_choices(),
        help="Filter by Scan status",
    )

    for date_field in ["completed", "started"]:
        for filter_lookup in ["gt", "gte", "lt", "lte"]:
            scan_filters_parser.add_argument(
                f"--f-{date_field}-{filter_lookup}",
                action="store",
                default=None,
                metavar="DATETIME",
                help=(
                    f"Filter Scans `{date_field}` datetime `{filter_lookup.upper()}` "
                    f"the specified date or datetime in ISO 8601 format. "
                    f"For example, `2020-07-05` for a date or `2020-07-05T12:45:30` for a datetime."
                ),
            )

    return scan_filters_parser


def build_scans_parser(commands_parser, configs_parser, file_parser, output_parser):
    scans_parser = commands_parser.add_parser(
        "scans",
        parents=[configs_parser],
        formatter_class=RichHelpFormatter,
    )
    scans_parser.set_defaults(
        command_handler=show_help,
        is_no_action_parser=True,
        parser=scans_parser,
        formatter_class=RichHelpFormatter,
    )

    scans_command_parser = scans_parser.add_subparsers()

    scan_filters_parser = build_scan_filters_parser()

    scans_cancel_parser = scans_command_parser.add_parser(
        "cancel",
        parents=[configs_parser, scan_filters_parser, output_parser],
        formatter_class=RichHelpFormatter,
    )
    scans_cancel_parser.add_argument(
        "scan_ids",
        metavar="SCAN_ID",
        nargs="*",
        help="IDs of scans to cancel",
        default=None,
    )
    scans_cancel_parser.set_defaults(
        command_handler=scans_cancel_command_handler,
        parser=scans_cancel_parser,
    )

    scans_get_parser = scans_command_parser.add_parser(
        "get",
        parents=[configs_parser, scan_filters_parser, output_parser],
        formatter_class=RichHelpFormatter,
    )
    scans_get_parser.add_argument(
        "scan_ids",
        metavar="SCAN_ID",
        nargs="*",
        help="IDs of Scans to list",
        default=None,
    )
    scans_get_parser.set_defaults(
        command_handler=scans_get_command_handler,
        parser=scans_get_parser,
    )

    scans_resume_parser = scans_command_parser.add_parser(
        "resume",
        parents=[configs_parser, scan_filters_parser, output_parser],
        formatter_class=RichHelpFormatter,
    )
    scans_resume_parser.add_argument(
        "scan_ids",
        metavar="SCAN_ID",
        nargs="*",
        help="IDs of scans to resume",
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
    scans_pause_parser = scans_command_parser.add_parser(
        "pause",
        parents=[configs_parser, scan_filters_parser, output_parser],
        formatter_class=RichHelpFormatter,
    )
    scans_pause_parser.add_argument(
        "scan_ids",
        metavar="SCAN_ID",
        nargs="*",
        help="IDs of scans to pause",
        default=None,
    )
    scans_pause_parser.set_defaults(
        command_handler=scans_pause_command_handler,
        parser=scans_pause_parser,
    )
