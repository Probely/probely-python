import argparse

from rich_argparse import RichHelpFormatter

from probely_cli.cli.commands.apply.apply import apply_command_handler
from probely_cli.cli.commands.scans.start import start_scans_command_handler
from probely_cli.cli.commands.targets.add import add_targets_command_handler
from probely_cli.cli.commands.targets.get import targets_get_command_handler
from probely_cli.cli.common import (
    TargetRiskEnum,
    TargetTypeEnum,
    lowercase_acceptable_parser_type,
    show_help,
    OutputEnum,
)
from probely_cli.settings import TRUTHY_VALUES, FALSY_VALUES


def build_targets_filters_parser():
    target_filters_parser = argparse.ArgumentParser(
        description="Filters usable in Targets commands",
        add_help=False,
        formatter_class=RichHelpFormatter,
    )

    multiple_values_help_text = (
        "You can chose multiple options separated by space. eg: '--f Value1 Value2'"
    )

    target_filters_parser.add_argument(
        "--f-has-unlimited-scans",
        type=lowercase_acceptable_parser_type,
        choices=TRUTHY_VALUES + FALSY_VALUES,
        help="Filter if target has unlimited scans. ",
        action="store",
        default=None,
    )
    target_filters_parser.add_argument(
        "--f-is-url-verified",
        type=lowercase_acceptable_parser_type,
        choices=TRUTHY_VALUES + FALSY_VALUES,
        help="Filter if target URL is verified. ",
        action="store",
        default=None,
    )

    target_filters_parser.add_argument(
        "--f-risk",
        type=lowercase_acceptable_parser_type,
        choices=TargetRiskEnum.cli_input_choices(),
        help="Filter targets by risk. " + multiple_values_help_text,
        nargs="+",
        action="store",
    )

    target_filters_parser.add_argument(
        "--f-type",
        type=lowercase_acceptable_parser_type,
        choices=TargetTypeEnum.cli_input_choices(),
        help="Filter targets by type. " + multiple_values_help_text,
        nargs="+",
        action="store",
    )

    target_filters_parser.add_argument(
        "--f-search",
        help="Keyword to match with name, url and labels",
        action="store",
        default=None,
    )

    return target_filters_parser


def build_targets_parser(
    commands_parser,
    configs_parser,
    file_parser,
    output_parser,
):
    target_filters_parser = build_targets_filters_parser()

    targets_parser = commands_parser.add_parser(
        "targets",
        parents=[configs_parser],
        formatter_class=RichHelpFormatter,
    )

    targets_parser.set_defaults(
        command_handler=show_help,
        is_no_action_parser=True,
        parser=targets_parser,
        formatter_class=RichHelpFormatter,
    )
    targets_command_parser = targets_parser.add_subparsers()

    targets_get_parser = targets_command_parser.add_parser(
        "get",
        parents=[configs_parser, target_filters_parser, output_parser],
        formatter_class=RichHelpFormatter,
    )

    targets_get_parser.add_argument(
        "target_ids",
        metavar="target_id",
        nargs="*",
        help="IDs of targets to list",
        default=None,
    )

    targets_get_parser.set_defaults(
        parser=targets_get_parser,
        command_handler=targets_get_command_handler,
    )

    targets_create_parser = targets_command_parser.add_parser(
        "add",
        parents=[configs_parser, file_parser],
        formatter_class=RichHelpFormatter,
    )

    targets_create_parser.add_argument(
        "site_url",
    )
    targets_create_parser.add_argument(
        "--site-name",
    )

    targets_create_parser.set_defaults(
        command_handler=add_targets_command_handler,
        parser=targets_create_parser,
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

    # TODO: kill in exchange of -o/--output option
    raw_response_parser = argparse.ArgumentParser(
        description="Returns JSON http response",
        add_help=False,
        formatter_class=RichHelpFormatter,
    )
    raw_response_parser.add_argument(
        "--raw",
        help="Show raw JSON api response",
        action="store_true",
        default=False,
    )

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

    build_targets_parser(
        commands_parser,
        configs_parser,
        file_parser,
        output_parser,
    )

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
        parents=[configs_parser, raw_response_parser, file_parser],
        formatter_class=probely_parser.formatter_class,
    )
    scans_start_parser.add_argument(
        "target_id",
    )
    scans_start_parser.set_defaults(
        command_handler=start_scans_command_handler,
        parser=scans_start_parser,
    )

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
