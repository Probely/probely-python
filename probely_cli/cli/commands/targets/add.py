import logging

from rich.console import Console

from probely_cli import sdk, ProbelyException, ProbelyBadRequest
from probely_cli.cli.common import validate_and_retrieve_yaml_content

err_console = Console(stderr=True)
console = Console()


logger = logging.getLogger(__name__)


def add_targets(args):
    site_url = args.site_url
    site_name = args.site_name
    yaml_file_path = args.yaml_file_path

    extra_payload = {}
    if yaml_file_path:  # TODO: validate is correct file
        extra_payload = validate_and_retrieve_yaml_content(yaml_file_path)

    logger.debug("extra_payload: {}".format(extra_payload))

    try:
        target: dict = sdk.add_target(
            site_url,
            site_name=site_name,
            extra_payload=extra_payload,
        )
    except ProbelyException as probely_ex:
        err_console.print(str(probely_ex))
        if isinstance(probely_ex, ProbelyBadRequest):
            err_console.print(probely_ex.response_payload)
        return

    if args.raw:
        console.print(target)
        return

    console.print(target["id"])
