import argparse
from rich_argparse import RichHelpFormatter

from probely_cli.cli.commands.targets.create import create_targets
from probely_cli.cli.commands.targets.list import list_targets
from probely_cli.cli.common import show_help

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

probely_parser = argparse.ArgumentParser(
    prog="Probely",
    description="Welcome to Probely's CLI",
    formatter_class=RichHelpFormatter,
)
probely_parser.set_defaults(
    func=show_help,
    is_no_action_parser=True,
    parser=probely_parser,
)

commands_parser = probely_parser.add_subparsers()

targets_parser = commands_parser.add_parser("targets")
targets_parser.set_defaults(
    func=show_help,
    is_no_action_parser=True,
    parser=targets_parser,
)
targets_command_parser = targets_parser.add_subparsers()

targets_list_parser = targets_command_parser.add_parser(
    "list",
    parents=[configs_parser],
    # formatter_class=probely_parser.formatter_class,
)
targets_list_parser.add_argument(
    "--count-only",
    action="store_true",
    help="Returns count of target",
)
targets_list_parser.add_argument(
    "--raw",
    action="store_true",
    help="Return JSON Objects as the API response",
)
targets_list_parser.set_defaults(func=list_targets)

targets_create_parser = targets_command_parser.add_parser(
    "create",
    parents=[configs_parser],
    # formatter_class=probely_parser.formatter_class,
)
targets_create_parser.set_defaults(func=create_targets)
