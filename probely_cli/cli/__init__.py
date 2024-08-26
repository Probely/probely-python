import logging
import sys
from argparse import Namespace

from rich.console import Console

from .app import CliApp
from .commands.parsers import build_cli_parser

logger = logging.getLogger(__name__)

console = Console(
    width=sys.maxsize,  # avoids word wrapping
)
err_console = Console(
    width=sys.maxsize,  # avoids word wrapping
    stderr=True,
)


def app():
    cli_parser = build_cli_parser()
    args: Namespace = cli_parser.parse_args()
    args.cli_parser = cli_parser
    args.console = console
    args.err_console = err_console

    cli_app = CliApp(args)

    from .. import settings

    logging_level = logging.DEBUG if settings.IS_DEBUG_MODE else logging.WARNING
    logging.basicConfig(level=logging_level)
    logger.debug("DEBUG MODE IS ON")

    return cli_app.run()
