import logging

from probely_cli.cli.common import validate_and_retrieve_yaml_content
from probely_cli.sdk.scans import start_scan

logger = logging.getLogger(__name__)


def start_scans_command_handler(args):
    target_id = args.target_id
    yaml_file_path = args.yaml_file_path

    logger.debug("Starting scan for target id: {}".format(target_id))

    extra_payload = {}
    if yaml_file_path:
        extra_payload = validate_and_retrieve_yaml_content(yaml_file_path)
    scan = start_scan(target_id, extra_payload)

    if args.raw:
        args.console.print(scan)
        return

    args.console.print(scan["id"])
