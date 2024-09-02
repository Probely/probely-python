import sys
from io import StringIO
from pathlib import Path
from typing import Callable, Dict, List, Tuple, Union

import pytest
import yaml
from rich.console import Console

from probely_cli.cli import CliApp, build_cli_parser
from tests.testable_api_responses import (
    CANCEL_SCAN_200_RESPONSE,
    START_SCAN_200_RESPONSE,
    GET_TARGETS_200_RESPONSE,
    GET_FINDINGS_200_RESPONSE,
)


@pytest.fixture
def cli_parser():
    command_parser = build_cli_parser()
    return command_parser


def prepare_cmd_command_for_parsing(cmd_command: Union[str, Tuple[str]]) -> List[str]:
    """
    This adds some flexibility to the way we call commands using the probely_cli fixture.
    All the following options are valid:
    "probely targets get --f-risk NA"
    "targets get --f-risk NA"
    ["probely", "targets", "get", "--f-risk NA"]
    ["targets", "get", "--f-risk NA"]
    ["targets", "get", "--f-risk", "NA"]
    etc..
    """

    prepared_cmd_command = []
    for item in cmd_command:
        if " " in item:
            prepared_cmd_command.extend(item.split())
            continue

        prepared_cmd_command.append(item)

    if prepared_cmd_command[0] == "probely":
        # In cmd command "probely" is to call the script, we don't need it as we're it
        prepared_cmd_command.pop(0)

    return prepared_cmd_command


@pytest.fixture
def probely_cli(cli_parser, capsys):
    def run_command(*cmd_command: Union[str, Tuple[str]], return_list=False):

        if len(cmd_command) == 0:
            raise pytest.UsageError("probely_cli can't run without cmd_command")

        testable_console = Console(
            file=StringIO(),
            width=sys.maxsize,  # avoids word wrapping
        )
        testable_err_console = Console(
            stderr=True,
            file=StringIO(),
            width=sys.maxsize,  # avoids word wrapping
        )

        cmd_as_list = prepare_cmd_command_for_parsing(cmd_command)

        try:
            args = cli_parser.parse_args(cmd_as_list)
            args.console = testable_console
            args.err_console = testable_err_console
            cli_app = CliApp(args)
            cli_app.run()

            # noinspection PyUnresolvedReferences
            raw_stdout: str = testable_console.file.getvalue()
            # noinspection PyUnresolvedReferences
            raw_stderr: str = testable_err_console.file.getvalue()

        except SystemExit:  # meaning the argparse found an error
            # argparse writes directly to std.err and exist execution
            # when a parsing error is found
            raw_stdout, raw_stderr = capsys.readouterr()

        if return_list:
            stdout_lines_list = raw_stdout.splitlines()
            stderr_lines_list = raw_stderr.splitlines()

            return stdout_lines_list, stderr_lines_list

        return raw_stdout, raw_stderr

    return run_command


@pytest.fixture()
def create_testable_yaml_file(tmp_path: Path) -> Callable:
    """
    Returns function that generates temporary yaml file ideal
    to test file parameter of CLI commands.
    """

    def _create_testable_yaml_file(file_name: str, file_content: Dict) -> str:
        yaml_content = yaml.dump(file_content)

        testable_yaml_file: Path = tmp_path / file_name
        testable_yaml_file.write_text(yaml_content)

        return str(testable_yaml_file)

    return _create_testable_yaml_file


@pytest.fixture()
def valid_scans_start_api_response() -> dict:
    return START_SCAN_200_RESPONSE


@pytest.fixture()
def valid_scans_cancel_api_response() -> dict:
    return CANCEL_SCAN_200_RESPONSE


@pytest.fixture()
def valid_get_targets_api_response() -> dict:
    return GET_TARGETS_200_RESPONSE


@pytest.fixture()
def valid_get_findings_api_response() -> dict:
    return GET_FINDINGS_200_RESPONSE
