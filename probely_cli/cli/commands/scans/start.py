import logging

from probely_cli.sdk.scans import start_scan
from rich.console import Console

console = Console()


logger = logging.getLogger(__name__)


def start_scans_command_handler(args):
    target_id = args.target_id

    logger.debug("Starting scan for target id: {}".format(target_id))

    body = {}
    # TODO: option to add extra payload
    scan = start_scan(target_id, body)

    if args.raw:
        console.print(scan)

    console.print(scan["id"])
