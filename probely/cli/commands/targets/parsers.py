import argparse

from rich_argparse import RichHelpFormatter

from probely.cli.commands.targets.add import targets_add_command_handler
from probely.cli.commands.targets.delete import targets_delete_command_handler
from probely.cli.commands.targets.get import targets_get_command_handler
from probely.cli.commands.targets.start_scan import start_scans_command_handler
from probely.cli.commands.targets.update import update_targets_command_handler
from probely.cli.common import show_help
from probely.sdk.enums import (
    TargetAPISchemaTypeEnum,
    TargetRiskEnum,
    TargetTypeEnum,
)
from probely.settings import FALSY_VALUES, TRUTHY_VALUES


def build_targets_filters_parser() -> argparse.ArgumentParser:
    target_filters_parser = argparse.ArgumentParser(
        description="Filters usable in Targets commands",
        add_help=False,
        formatter_class=RichHelpFormatter,
    )
    target_filters_parser.add_argument(
        "--f-has-unlimited-scans",
        type=str.upper,
        choices=TRUTHY_VALUES + FALSY_VALUES,
        help="Filter if target has unlimited scans",
        action="store",
    )
    target_filters_parser.add_argument(
        "--f-is-url-verified",
        type=str.upper,
        choices=TRUTHY_VALUES + FALSY_VALUES,
        help="Filter if target URL is verified",
        action="store",
    )
    target_filters_parser.add_argument(
        "--f-risk",
        type=str.upper,
        choices=TargetRiskEnum.cli_input_choices(),
        help="Filter targets by list of risk",
        nargs="+",
        action="store",
    )
    target_filters_parser.add_argument(
        "--f-type",
        type=str.upper,
        choices=TargetTypeEnum.cli_input_choices(),
        help="Filter targets by list of type",
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


def build_targets_parser(commands_parser, configs_parser, file_parser, output_parser):

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
        metavar="TARGET_ID",
        nargs="*",
        help="IDs of Targets to list",
        default=None,
    )
    targets_get_parser.set_defaults(
        command_handler=targets_get_command_handler,
        parser=targets_get_parser,
    )

    targets_delete_parser = targets_command_parser.add_parser(
        "delete",
        parents=[configs_parser, target_filters_parser],
        formatter_class=RichHelpFormatter,
    )
    targets_delete_parser.add_argument(
        "target_ids",
        metavar="TARGET_ID",
        nargs="*",
        help="IDs of targets to delete",
        default=None,
    )
    targets_delete_parser.set_defaults(
        command_handler=targets_delete_command_handler,
        parser=targets_delete_parser,
    )

    targets_add_parser = targets_command_parser.add_parser(
        "add",
        parents=[configs_parser, file_parser, output_parser],
        formatter_class=RichHelpFormatter,
    )
    targets_add_parser.add_argument(
        "target_url",
        metavar="TARGET_URL",
        nargs="?",
        help="Url of target",
    )
    targets_add_parser.add_argument(
        "--target-name",
        help="Display name of target",
    )
    targets_add_parser.add_argument(
        "--target-type",
        type=str.upper,
        choices=TargetTypeEnum.cli_input_choices(),
        help="Type of target",
    )
    targets_add_parser.add_argument(
        "--api-schema-type",
        type=str.upper,
        choices=TargetAPISchemaTypeEnum.cli_input_choices(),
        help="Type of schema for API Targets",
    )
    targets_add_parser.add_argument(
        "--api-schema-file-url",
        help="Url for download of API schema of target",
    )
    targets_add_parser.set_defaults(
        command_handler=targets_add_command_handler,
        parser=targets_add_parser,
    )

    targets_update_parser = targets_command_parser.add_parser(
        "update",
        parents=[configs_parser, target_filters_parser, file_parser, output_parser],
        formatter_class=RichHelpFormatter,
    )
    targets_update_parser.add_argument(
        "target_ids",
        metavar="TARGET_ID",
        nargs="*",
        help="IDs of targets to update",
        default=None,
    )
    targets_update_parser.set_defaults(
        command_handler=update_targets_command_handler,
        parser=targets_update_parser,
    )

    start_scan_parser = targets_command_parser.add_parser(
        "start-scan",
        parents=[configs_parser, target_filters_parser, file_parser, output_parser],
        formatter_class=RichHelpFormatter,
    )
    start_scan_parser.add_argument(
        "target_ids",
        metavar="TARGET_ID",
        nargs="*",
        help="IDs of Targets that will be scanned",
        default=None,
    )
    start_scan_parser.set_defaults(
        command_handler=start_scans_command_handler,
        parser=start_scan_parser,
    )
