import argparse

from probely_cli import settings


class CliApp:
    args: argparse.Namespace

    def __init__(self, args: argparse.Namespace):
        args_dict = vars(args)
        if args_dict.get("api_key"):
            settings.PROBELY_API_KEY = args.api_key

        if args_dict.get("debug"):
            settings.IS_DEBUG_MODE = True

        self.args = args

    def run(self):
        try:
            return self.args.func(self.args)
        except Exception as e:
            self.args.err_console.print(e)
