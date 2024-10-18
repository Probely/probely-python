import argparse

from rich_argparse import RichHelpFormatter

from probely.cli.commands.findings.parsers import build_findings_parser
from probely.cli.commands.scans.parsers import build_scans_parser
from probely.cli.commands.targets.parsers import build_targets_parser
from probely.cli.common import show_help
from probely.cli.enums import OutputEnum
from probely.version import __version__


def build_file_parser():
    file_parser = argparse.ArgumentParser(
        description="File allowing to send customized payload to Probely's API",
        add_help=False,
        formatter_class=RichHelpFormatter,
    )
    file_parser.add_argument(
        "-f",
        "--yaml-file",
        dest="yaml_file_path",
        default=None,
        help="Path to file with content to apply. Accepts same payload as listed in API docs",
    )

    return file_parser


def build_configs_parser():
    configs_parser = argparse.ArgumentParser(
        description="Configs settings parser",
        add_help=False,  # avoids conflicts with --help child command
        formatter_class=RichHelpFormatter,
    )
    configs_parser.add_argument(
        "--api-key",
        help="Authorization token to make requests to the API",
        default=None,
    )
    configs_parser.add_argument(
        "--debug",
        help="Enables debug mode setting",
        action="store_true",
        default=False,
    )
    return configs_parser


def build_output_parser():
    output_parser = argparse.ArgumentParser(
        description="Controls output format of command",
        formatter_class=RichHelpFormatter,
        add_help=False,
    )
    output_parser.add_argument(
        "-o",
        "--output",
        type=str.upper,
        choices=OutputEnum.cli_input_choices(),
        help="Changes the output formats based on presets",
    )
    return output_parser


def build_cli_parser():
    file_parser = build_file_parser()
    configs_parser = build_configs_parser()
    output_parser = build_output_parser()

    probely_parser = argparse.ArgumentParser(
        prog="probely",
        description="Probely's CLI. Check subcommands for available actions",
        formatter_class=RichHelpFormatter,
    )
    probely_parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    probely_parser.set_defaults(
        command_handler=show_help,
        is_no_action_parser=True,
        parser=probely_parser,
    )

    commands_parser = probely_parser.add_subparsers(
        title="Subcommands for available contexts"
    )

    build_targets_parser(commands_parser, configs_parser, file_parser, output_parser)
    build_scans_parser(commands_parser, configs_parser, file_parser, output_parser)
    build_findings_parser(commands_parser, configs_parser, output_parser)

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
