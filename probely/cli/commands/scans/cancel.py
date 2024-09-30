import logging

from probely.cli.commands.scans.schemas import ScanApiFiltersSchema
from probely.cli.common import (
    display_scans_response_output,
    prepare_filters_for_api,
)
from probely.exceptions import ProbelyCLIValidation
from probely.sdk.scans import cancel_scan, cancel_scans, list_scans

logger = logging.getLogger(__name__)


def scans_cancel_command_handler(args):
    scan_ids = args.scan_ids
    filters = prepare_filters_for_api(ScanApiFiltersSchema, args)

    if not scan_ids and not filters:
        raise ProbelyCLIValidation("Expected scan_ids or filters")

    if filters and scan_ids:
        raise ProbelyCLIValidation("Filters and Scan IDs are mutually exclusive")

    if filters:
        scan_list = list_scans(scans_filters=filters)
        searched_scan_ids = [scan.get("id") for scan in scan_list]

        if not searched_scan_ids:
            raise ProbelyCLIValidation("Selected Filters returned no results")

        scan_ids = searched_scan_ids

    logger.debug("Cancelling scan for scan ids: {}".format(scan_ids))

    scans = []
    if len(scan_ids) == 1:
        scan = cancel_scan(scan_ids[0])
        scans.append(scan)
    else:
        scans = cancel_scans(scan_ids)

    display_scans_response_output(args, scans)
