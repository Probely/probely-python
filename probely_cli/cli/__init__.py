import logging

from argparse import Namespace

from .commands.parsers import probely_parser
from .common import CliApp
from ..settings import DEBUG_MODE

if DEBUG_MODE:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARNING)


logger = logging.getLogger(__name__)


def app():
    args: Namespace = probely_parser.parse_args()

    logger.debug("DEBUG MODE IS ON")
    cli_app = CliApp(args)

    return cli_app.run(args.func)
