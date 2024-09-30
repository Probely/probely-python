import logging

from probely.cli.commands.scans.schemas import ScanApiFiltersSchema
from probely.cli.common import (
    display_scans_response_output,
    prepare_filters_for_api,
)
from probely.exceptions import ProbelyCLIValidation
from probely.sdk.scans import list_scans, pause_scan, pause_scans

logger = logging.getLogger(__name__)


def scans_pause_command_handler(args):
    filters = prepare_filters_for_api(ScanApiFiltersSchema, args)
    scan_ids = args.scan_ids

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

    logger.debug("Pausing scan for scan ids: {}".format(scan_ids))
    scans = []
    if len(scan_ids) == 1:
        scan = pause_scan(scan_ids[0])
        scans.append(scan)
    else:
        scans = pause_scans(scan_ids)
    display_scans_response_output(args, scans)
