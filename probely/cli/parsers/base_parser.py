from probely.cli.parsers.common import ProbelyArgumentParser, show_help
from probely.cli.parsers.findings_parsers import build_findings_parser
from probely.cli.parsers.help_texts import (
    TARGET_COMMAND_DESCRIPTION_TEXT,
    SCANS_COMMAND_DESCRIPTION_TEXT,
    FINDINGS_COMMAND_DESCRIPTION_TEXT,
)
from probely.cli.parsers.scans_parsers import build_scans_parser
from probely.cli.parsers.targets_parsers import build_targets_parser
from probely.version import __version__


def build_cli_parser():

    targets_subcommand_parser = build_targets_parser()
    scans_subcommand_parser = build_scans_parser()
    findings_subcommand_parser = build_findings_parser()

    probely_parser = ProbelyArgumentParser(
        prog="probely",
        description="Probely's CLI. Check subcommands for available actions",
    )
    probely_parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    probely_parser.set_defaults(
        command_handler=show_help,
        is_no_action_parser=True,
        parser=probely_parser,
    )

    subcommands_parser = probely_parser.add_subparsers(
        title="Subcommands for available contexts"
    )

    subcommands_parser.add_parser(
        name="targets",
        parents=[targets_subcommand_parser],
        help=TARGET_COMMAND_DESCRIPTION_TEXT,
    )
    subcommands_parser.add_parser(
        name="scans",
        parents=[scans_subcommand_parser],
        help=SCANS_COMMAND_DESCRIPTION_TEXT,
    )
    subcommands_parser.add_parser(
        name="findings",
        parents=[findings_subcommand_parser],
        help=FINDINGS_COMMAND_DESCRIPTION_TEXT,
    )

    # apply_parser = commands_parser.add_parser(
    #     "apply",
    #     parents=[configs_parser],
    #     formatter_class=RichHelpFormatter,
    # )
    # apply_parser.add_argument("yaml_file")
    # apply_parser.set_defaults(
    #     command_handler=apply_command_handler,
    #     parser=apply_parser,
    # )

    return probely_parser
