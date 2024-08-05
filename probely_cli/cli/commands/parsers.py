import argparse
from rich_argparse import RichHelpFormatter

from probely_cli.cli.commands.apply.apply import apply_command_handler
from probely_cli.cli.commands.scans.start import start_scans_command_handler
from probely_cli.cli.commands.targets.add import add_targets_command_handler
from probely_cli.cli.commands.targets.get import targets_get_command_handler
from probely_cli.cli.common import show_help, TargetRiskEnum, TargetTypeEnum


def build_targets_parser(
    commands_parser,
    configs_parser,
    file_parser,
):

    target_filters_parser = argparse.ArgumentParser(
        description="Filters usable in Targets commands",
        add_help=False,
        formatter_class=RichHelpFormatter,
    )

    bool_input_help_text = (
        "Accepts falsy/truly values: 'true', 'false', 't', 'f', 'yes', 'no', etc"
    )
    multiple_values_help_text = (
        "You can select multiple values separated by comma. eg: Value1, Value2"
    )

    target_filters_parser.add_argument(
        "--f-has-unlimited-scans",
        help="Filter if target has unlimited scans. " + bool_input_help_text,
        action="store",
        default=None,
    )
    target_filters_parser.add_argument(
        "--f-is-url-verified",
        help="Filter if target URL has verification. " + bool_input_help_text,
        action="store",
        default=None,
    )

    accepted_risk_values = ", ".join([str(risk.name) for risk in TargetRiskEnum])
    accepted_risk_values_help_text = "Accepted values: " + accepted_risk_values + ". "

    target_filters_parser.add_argument(
        "--f-risk",
        help="Filter targets by risk. "
        + accepted_risk_values_help_text
        + multiple_values_help_text,
        action="store",
        default=None,
    )

    accepted_type_values = ", ".join([str(risk.name) for risk in TargetTypeEnum])
    accepted_risk_values_help_text = "Accepted values: " + accepted_type_values + ". "

    target_filters_parser.add_argument(
        "--f-type",
        help="Filter targets by type. "
        + accepted_risk_values_help_text
        + multiple_values_help_text,
        action="store",
        default=None,
    )

    target_filters_parser.add_argument(
        "--f-search",
        help="Keyword to match with name, url and labels",
        action="store",
        default=None,
    )

    targets_parser = commands_parser.add_parser(
        "targets",
        parents=[configs_parser],
        formatter_class=RichHelpFormatter,
    )
    targets_parser.set_defaults(
        func=show_help,
        is_no_action_parser=True,
        parser=targets_parser,
        formatter_class=RichHelpFormatter,
    )
    targets_command_parser = targets_parser.add_subparsers()

    targets_list_parser = targets_command_parser.add_parser(
        "get",
        parents=[configs_parser, target_filters_parser],
        formatter_class=RichHelpFormatter,
    )

    targets_list_parser.set_defaults(func=targets_get_command_handler)

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
        default=None,
    )

    targets_create_parser.set_defaults(func=add_targets_command_handler)


def build_cli_parser():
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

    probely_parser = argparse.ArgumentParser(
        prog="probely",
        description="Welcome to Probely's CLI",
        formatter_class=RichHelpFormatter,
    )
    probely_parser.set_defaults(
        func=show_help,
        is_no_action_parser=True,
        parser=probely_parser,
    )

    commands_parser = probely_parser.add_subparsers()

    build_targets_parser(
        commands_parser,
        configs_parser,
        file_parser,
    )

    scans_parser = commands_parser.add_parser(
        "scans",
        parents=[configs_parser],
        formatter_class=RichHelpFormatter,
    )

    scans_parser.set_defaults(
        func=show_help,
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
    scans_start_parser.set_defaults(func=start_scans_command_handler)

    apply_parser = commands_parser.add_parser(
        "apply",
        parents=[configs_parser],
        formatter_class=RichHelpFormatter,
    )
    apply_parser.add_argument("yaml_file")
    apply_parser.set_defaults(
        func=apply_command_handler,
    )

    return probely_parser
