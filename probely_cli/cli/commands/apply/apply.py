import logging
from pathlib import Path

from rich.console import Console
from probely_cli.sdk.targets import add_target
from probely_cli.exceptions import (
    ProbelyException,
    ProbelyBadRequest,
)
from probely_cli.cli.commands.apply.schemas import ApplyFileSchema
from probely_cli.cli.common import validate_and_retrieve_yaml_content

err_console = Console(stderr=True)
console = Console()

logger = logging.getLogger(__name__)


def apply_command_handler(args):
    """
    This is a test

    :param args:
    """
    yaml_file_path: Path = Path(args.yaml_file)

    yaml_content = validate_and_retrieve_yaml_content(yaml_file_path)

    ApplyFileSchema().validate(yaml_content)
    logger.debug("Valid yaml_file content. Executing actions")

    action = yaml_content["action"]
    payload = yaml_content["payload"]

    if action == "add_target":
        logger.debug("Performing action 'add_target' with payload: {}".format(payload))
        try:
            # TODO: This is the same as in add_targets(). abstract?
            url = payload["site"]["url"]
            target = add_target(url, extra_payload=payload)
            console.print(target["id"])
        except ProbelyException as probely_ex:
            err_console.print(str(probely_ex))
            if isinstance(probely_ex, ProbelyBadRequest):
                err_console.print(str(probely_ex.response_payload))
