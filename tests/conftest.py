import sys
from io import StringIO
from pathlib import Path
from typing import Callable, Dict, List

import pytest
import yaml
from rich.console import Console

from probely_cli.cli import build_cli_parser
from tests.testable_api_responses import (
    START_SCAN_200_RESPONSE,
    GET_TARGETS_200_RESPONSE,
)


@pytest.fixture
def cli_parser():
    command_parser = build_cli_parser()
    return command_parser


@pytest.fixture
def probely_cli(cli_parser, capsys):
    def run_command(*cmd_command: List[str], return_list=False):
        testable_console = Console(
            file=StringIO(),
            width=sys.maxsize,  # avoids word wrapping
        )
        testable_err_console = Console(
            file=StringIO(),
            width=sys.maxsize,  # avoids word wrapping
        )

        args = cli_parser.parse_args(cmd_command)
        args.console = testable_console
        args.err_console = testable_err_console
        args.func(args)

        # noinspection PyUnresolvedReferences
        raw_stdout = testable_console.file.getvalue()
        # noinspection PyUnresolvedReferences
        raw_stderr = testable_err_console.file.getvalue()

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
def valid_get_targets_api_response() -> dict:
    return GET_TARGETS_200_RESPONSE
