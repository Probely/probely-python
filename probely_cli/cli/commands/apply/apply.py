import logging
from pathlib import Path

import yaml
from rich.console import Console

from probely_cli import sdk, ProbelyException, ProbelyBadRequest, ProbelyCLIValidation
from probely_cli.cli.commands.apply.schemas import ApplyFileSchema
from probely_cli.settings import CLI_ACCEPTED_FILE_EXTENSIONS

err_console = Console(stderr=True)
console = Console()

logger = logging.getLogger(__name__)


def apply_file(args):
    yaml_file_path: Path = Path(args.yaml_file)

    if not yaml_file_path.exists():
        raise ProbelyCLIValidation(
            "Provided path does not exist: {}".format(yaml_file_path)
        )

    if not yaml_file_path.is_file():
        raise ProbelyCLIValidation(
            "Provided path is not a file: {}".format(yaml_file_path.absolute())
        )

    if yaml_file_path.suffix not in CLI_ACCEPTED_FILE_EXTENSIONS:
        raise ProbelyCLIValidation(
            "Invalid file extension, must be one of the following: {}:".format(
                CLI_ACCEPTED_FILE_EXTENSIONS
            )
        )

    with yaml_file_path.open() as yaml_file:
        try:
            # I need to validate and make sure what versions of yaml we support
            yaml_content = yaml.safe_load(yaml_file)
        except yaml.scanner.ScannerError as ex:
            raise ProbelyCLIValidation("Yaml file content is invalid: {}".format(ex))

    ApplyFileSchema().validate(yaml_content)
    logger.debug("Valid yaml_file content. Executing actions")

    action = yaml_content["action"]
    payload = yaml_content["payload"]

    if action == "add_target":
        logger.debug("Performing action 'add_target' with payload: {}".format(payload))
        try:
            # TODO: This is the same as in add_targets(). abstract?
            url = payload["site"]["url"]
            target = sdk.add_target(url, extra_payload=payload)
            console.print(target["id"])
        except ProbelyException as probely_ex:
            err_console.print(str(probely_ex))
            if isinstance(probely_ex, ProbelyBadRequest):
                err_console.print(str(probely_ex.response_payload))
