import logging
from argparse import Namespace

from .commands.parsers import probely_parser
from .common import CliApp

logger = logging.getLogger(__name__)


def app():
    args: Namespace = probely_parser.parse_args()

    cli_app = CliApp(args)

    from .. import settings

    logging_level = logging.DEBUG if settings.IS_DEBUG_MODE else logging.WARNING
    logging.basicConfig(level=logging_level)
    logger.debug("DEBUG MODE IS ON")

    return cli_app.run(args.func)
