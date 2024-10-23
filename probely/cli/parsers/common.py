import argparse
from typing import Type

import rich_argparse

from probely.cli.enums import OutputEnum


class ProbelyArgumentParser(argparse.ArgumentParser):
    def __init__(
        self,
        *args,
        formatter_class: Type[argparse.HelpFormatter] = None,
        **kwargs,
    ):
        if not formatter_class:
            formatter_class = rich_argparse.RichHelpFormatter

        super().__init__(*args, formatter_class=formatter_class, **kwargs)


def show_help(args):
    if args.is_no_action_parser:
        args.parser.print_help()


def build_file_parser():
    file_parser = ProbelyArgumentParser(
        add_help=False,  # avoids conflicts with --help child command
        description="File allowing to send customized payload to Probely's API",
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
    configs_parser = ProbelyArgumentParser(
        add_help=False,  # avoids conflicts with --help child command
        description="Configs settings parser",
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
    output_parser = ProbelyArgumentParser(
        add_help=False,  # avoids conflicts with --help child command
        description="Controls output format of command",
    )
    output_parser.add_argument(
        "-o",
        "--output",
        type=str.upper,
        choices=OutputEnum.cli_input_choices(),
        help="Changes the output formats based on presets",
    )
    return output_parser
