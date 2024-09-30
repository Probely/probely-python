import logging

from probely.cli.commands.apply.schemas import ApplyFileSchema
from probely.cli.common import validate_and_retrieve_yaml_content
from probely.exceptions import ProbelyBadRequest, ProbelyException
from probely.sdk.targets import add_target

logger = logging.getLogger(__name__)


def apply_command_handler(args):
    """
    This is a test

    :param args:
    """
    # TODO: add docstring
    yaml_file_path: str = args.yaml_file

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
            args.console.print(target["id"])
        except ProbelyException as probely_ex:
            args.err_console.print(str(probely_ex))
            if isinstance(probely_ex, ProbelyBadRequest):
                args.err_console.print(str(probely_ex.response_payload))
