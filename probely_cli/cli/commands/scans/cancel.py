import json
import logging
import sys
from typing import Dict, List

import yaml
from rich.table import Table

from probely_cli.cli.common import OutputEnum
from probely_cli.cli.formatters import get_printable_labels
from probely_cli.sdk.scans import cancel_scans

logger = logging.getLogger(__name__)


def scans_cancel_command_handler(args):
    scan_ids = args.scan_ids

    if not scan_ids:
        args.parser.print_help()
        return

    logger.debug("Cancelling scan for scan ids: {}".format(scan_ids))
    scans = cancel_scans(scan_ids)
    for scan in scans:
        args.console.print(scan.get("id"))
