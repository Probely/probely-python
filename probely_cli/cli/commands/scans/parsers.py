from rich_argparse import RichHelpFormatter

from probely_cli.cli.commands.scans.cancel import scans_cancel_command_handler
from probely_cli.cli.commands.scans.start import start_scans_command_handler
from probely_cli.cli.common import show_help


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

    scans_start_parser = scans_command_parser.add_parser(
        "start",
        parents=[configs_parser, file_parser],
        formatter_class=RichHelpFormatter,
    )
    scans_start_parser.add_argument(
        "target_id",
    )
    scans_start_parser.set_defaults(
        command_handler=start_scans_command_handler,
        parser=scans_start_parser,
    )

    scans_cancel_parser = scans_command_parser.add_parser(
        "cancel",
        parents=[configs_parser, output_parser],
        formatter_class=RichHelpFormatter,
    )
    scans_cancel_parser.add_argument(
        "scan_ids",
        metavar="scan_id",
        nargs="*",
        help="IDs of scans to cancel",
        default=None,
    )
    scans_cancel_parser.set_defaults(
        command_handler=scans_cancel_command_handler,
        parser=scans_cancel_parser,
    )
