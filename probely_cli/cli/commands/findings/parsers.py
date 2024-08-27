from rich_argparse import RichHelpFormatter

from probely_cli.cli.commands.findings.get import findings_get_command_handler
from probely_cli.cli.common import show_help


def build_findings_parser(commands_parser, configs_parser):

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
        parents=[configs_parser],
        formatter_class=RichHelpFormatter,
    )

    findings_get_parser.set_defaults(
        command_handler=findings_get_command_handler,
        parser=findings_get_parser,
    )
