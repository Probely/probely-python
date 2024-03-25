import argparse

from probely_cli import settings, ProbelyException
from functools import wraps

from rich.console import Console

err_console = Console(stderr=True)


def cli_exception_handler(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ProbelyException as e:
            err_console.print(e)

    return func_wrapper


class CliApp:
    args: argparse.Namespace

    def __init__(self, args: argparse.Namespace):
        args_dict = vars(args)
        if args_dict.get("api_key"):
            settings.PROBELY_API_KEY = args.api_key

        self.args = args

    @cli_exception_handler
    def run(self, func):
        return func(self.args)


def show_help(args):
    if args.is_no_action_parser:
        args.parser.print_help()
