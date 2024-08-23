import argparse
import logging

from probely_cli import settings
from probely_cli.exceptions import ProbelyException

logger = logging.getLogger(__name__)


class CliApp:
    args: argparse.Namespace

    def __init__(self, args: argparse.Namespace):
        args_dict = vars(args)
        if args_dict.get("api_key"):
            settings.PROBELY_API_KEY = args.api_key

        if args_dict.get("debug"):
            settings.IS_DEBUG_MODE = True

        self.args = args

    def _print_error_message(self, message: str) -> None:
        message = "{cmd}: error: {message}".format(
            cmd=self.args.parser.prog, message=message
        )
        self.args.err_console.print(message)

    def run(self):
        try:
            return self.args.command_handler(self.args)
        except ProbelyException as e:
            self._print_error_message(str(e))
        except Exception as e:
            logger.debug("Unhandled exception:")
            self._print_error_message(str(e))
