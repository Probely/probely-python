import logging

from probely_cli.cli.commands.scans.schemas import ScanApiFiltersSchema
from probely_cli.cli.common import (
    display_scans_response_output,
    prepare_filters_for_api,
)
from probely_cli.exceptions import ProbelyCLIValidation
from probely_cli.sdk.scans import list_scans, resume_scan, resume_scans

logger = logging.getLogger(__name__)


def scans_resume_command_handler(args):
    filters = prepare_filters_for_api(ScanApiFiltersSchema, args)
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
    scans = []
    if len(scan_ids) == 1:
        scan = resume_scan(scan_ids[0])
        scans.append(scan)
    else:
        scans = resume_scans(scan_ids, ignore_blackout_period=ignore_blackout_period)

    display_scans_response_output(args, scans)
