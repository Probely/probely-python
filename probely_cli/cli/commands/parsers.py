import argparse

from rich_argparse import RichHelpFormatter

from probely_cli.cli.commands.apply.apply import apply_command_handler
from probely_cli.cli.commands.findings.parsers import build_findings_parser
from probely_cli.cli.commands.scans.parsers import build_scans_parser
from probely_cli.cli.commands.targets.parsers import build_targets_parser
from probely_cli.cli.common import (
    lowercase_acceptable_parser_type,
    OutputEnum,
    show_help,
)


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
        help="Path to yaml file. Accepts same payload as listed in API docs",
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
        help="Override API KEY used for requests",
        default=None,
    )
    configs_parser.add_argument(
        "--debug",
        help="Override DEBUG MODE setting",
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
        "--output",
        "-o",
        type=lowercase_acceptable_parser_type,
        choices=OutputEnum.cli_input_choices(),
        help="Presets for output formats",
    )
    return output_parser


def build_cli_parser():
    file_parser = build_file_parser()
    configs_parser = build_configs_parser()
    output_parser = build_output_parser()

    probely_parser = argparse.ArgumentParser(
        prog="probely",
        description="Welcome to Probely's CLI",
        formatter_class=RichHelpFormatter,
    )
    probely_parser.set_defaults(
        command_handler=show_help,
        is_no_action_parser=True,
        parser=probely_parser,
    )

    commands_parser = probely_parser.add_subparsers()

    build_targets_parser(commands_parser, configs_parser, file_parser, output_parser)
    build_scans_parser(commands_parser, configs_parser, file_parser, output_parser)
    build_findings_parser(commands_parser, configs_parser)

    apply_parser = commands_parser.add_parser(
        "apply",
        parents=[configs_parser],
        formatter_class=RichHelpFormatter,
    )
    apply_parser.add_argument("yaml_file")
    apply_parser.set_defaults(
        command_handler=apply_command_handler,
        parser=apply_parser,
    )

    return probely_parser
