import logging

from probely_cli.cli.commands.scans.get import (
    prepare_scan_filters_for_api,
)
from probely_cli.cli.common import display_scans_response_output
from probely_cli.exceptions import ProbelyCLIValidation
from probely_cli.sdk.scans import list_scans, resume_scans

logger = logging.getLogger(__name__)


def scans_resume_command_handler(args):
    filters = prepare_scan_filters_for_api(args)
    scan_ids = args.scan_ids

    if not scan_ids and not filters:
        raise ProbelyCLIValidation("Expected scan_ids or filters")

    if filters and scan_ids:
        raise ProbelyCLIValidation("Filters and Scan IDs are mutually exclusive")

    ignore_blackout_period = args.ignore_blackout_period

    if filters:
        scan_list = list_scans(scans_filters=filters)
        scan_ids = [scan.get("id") for scan in scan_list]

    logger.debug("Resuming scan for scan ids: {}".format(scan_ids))
    scans = resume_scans(scan_ids, ignore_blackout_period=ignore_blackout_period)

    display_scans_response_output(args, scans)
