from argparse import Namespace

from .commands.parsers import probely_parser
from .common import CliApp


def app():
    args: Namespace = probely_parser.parse_args()

    cli_app = CliApp(args)

    return cli_app.run(args.func)
