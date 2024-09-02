import logging

from probely_cli.cli.common import validate_and_retrieve_yaml_content
from probely_cli.exceptions import ProbelyException, ProbelyBadRequest
from probely_cli.sdk.targets import add_target

logger = logging.getLogger(__name__)


def add_targets_command_handler(args):
    site_url = args.site_url
    site_name = args.site_name
    yaml_file_path = args.yaml_file_path

    extra_payload = {}
    if yaml_file_path:
        extra_payload = validate_and_retrieve_yaml_content(yaml_file_path)

    logger.debug("extra_payload: {}".format(extra_payload))

    try:
        target: dict = add_target(
            site_url,
            site_name=site_name,
            extra_payload=extra_payload,
        )
    except ProbelyException as probely_ex:
        args.err_console.print(str(probely_ex))
        if isinstance(probely_ex, ProbelyBadRequest):
            args.err_console.print(probely_ex.response_payload)
        return

    args.console.print(target["id"])
