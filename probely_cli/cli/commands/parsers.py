import argparse
from rich_argparse import RichHelpFormatter

from probely_cli.cli.commands.apply.apply import apply_file
from probely_cli.cli.commands.targets.add import add_targets
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

configs_parser.add_argument(
    "--debug",
    help="Override DEBUG MODE setting",
    action="store_true",
    default=False,
)

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

targets_parser = commands_parser.add_parser(
    "targets",
    parents=[configs_parser, raw_response_parser],
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
    "list",
    parents=[configs_parser, raw_response_parser],
    formatter_class=probely_parser.formatter_class,
    # formatter_class=probely_parser.formatter_class,
)
targets_list_parser.add_argument(
    "--count-only",
    action="store_true",
    help="Returns count of target",
)

targets_list_parser.set_defaults(func=list_targets)

targets_create_parser = targets_command_parser.add_parser(
    "add",
    parents=[configs_parser, raw_response_parser],
    formatter_class=RichHelpFormatter,
)

targets_create_parser.add_argument(
    "site_url",
)
targets_create_parser.add_argument(
    "--site-name",
    default=None,
)

targets_create_parser.add_argument(
    "-f",
    "--yaml-file",
    dest="yaml_file_path",
    default=None,
    help="Path to yaml file with target option. Accepts same options as in API docs",
)

targets_create_parser.set_defaults(func=add_targets)

apply_parser = commands_parser.add_parser(
    "apply",
    parents=[configs_parser, raw_response_parser],
    formatter_class=RichHelpFormatter,
)
apply_parser.add_argument("yaml_file")
apply_parser.set_defaults(
    func=apply_file,
)
