import json
from unittest.mock import MagicMock, patch

import pytest
import yaml

from probely.sdk.enums import TargetAPISchemaTypeEnum, TargetTypeEnum


@pytest.fixture
def targets__add__sdk_add_target_mock(valid_add_targets_api_response) -> MagicMock:
    with patch("probely.cli.commands.targets.add.add_target") as add_target_mock:
        add_target_mock.return_value = valid_add_targets_api_response
        yield add_target_mock


@pytest.mark.parametrize(
    "target_type",
    [
        "",  # should default to web
        "--target-type web",
        "--target-type api",
    ],
)
def test_targets_add__no_arguments_validation(
    targets__add__sdk_add_target_mock: MagicMock,
    target_type,
    probely_cli,
):
    stdout_lines, stderr_lines = probely_cli(
        "targets", "add", target_type, return_list=True
    )

    assert len(stdout_lines) == 0, "Expected no stdout when there are errors"
    assert stderr_lines[-1] == (
        "probely targets add: error: must provide a target URL by argument or yaml-file"
    ), "Expected error message with details"

    assert targets__add__sdk_add_target_mock.call_count == 0, "Expected no sdk calls"


@pytest.mark.parametrize(
    "testing_args,expected_error,assert_fail_msg",
    [
        (
            "--target-type API",
            "probely targets add: error: API targets require api_schema_file_url",
            "Expected error for lack of API schema file",
        ),
        (
            "--target-type API --api-schema-file-url file_url",
            "probely targets add: error: API schema file require api_schema_type",
            "Expected error for lack of API schema file type",
        ),
        (
            "--target-type API --api-schema-type OPENAPI",
            "probely targets add: error: API targets require api_schema_file_url",
            "Expected error for lack of API schema file",
        ),
    ],
)
def test_targets_add__api_target_argument_validation(
    targets__add__sdk_add_target_mock: MagicMock,
    testing_args,
    expected_error,
    assert_fail_msg,
    probely_cli,
):
    stdout_lines, stderr_lines = probely_cli(
        "targets", "add", "https://example.com", testing_args, return_list=True
    )

    assert len(stdout_lines) == 0, "Expected no output, only errors"
    assert stderr_lines[-1] == expected_error, assert_fail_msg
    assert targets__add__sdk_add_target_mock.call_count == 0


@pytest.mark.parametrize(
    "file_content, expected_error, assert_fail_msg",
    [
        (
            {},
            "error: must provide a target URL by argument or yaml-file",
            "Expected error for lack of site url",
        ),
        (
            {
                "type": TargetTypeEnum.API.api_request_value,
                "site": {
                    "url": "https://example.com",
                },
            },
            "error: API targets require api_schema_file_url",
            "Expected error for lack of API schema file",
        ),
        (
            {
                "type": TargetTypeEnum.API.api_request_value,
                "site": {
                    "url": "https://example.com",
                    "api_scan_settings": {
                        "api_schema_url": "www.schema_url.com",
                    },
                },
            },
            "error: API schema file require api_schema_type",
            "Expected error for lack of API schema file type",
        ),
        (
            {
                "type": TargetTypeEnum.API.api_request_value,
                "site": {
                    "url": "https://example.com",
                    "api_scan_settings": {
                        "api_schema_type": TargetAPISchemaTypeEnum.OPENAPI.api_request_value,
                    },
                },
            },
            "error: API targets require api_schema_file_url",
            "Expected error for lack of API schema file url",
        ),
        (
            {
                "type": TargetTypeEnum.API.api_request_value,
                "site": {
                    "url": "https://example.com",
                    "api_scan_settings": {
                        "api_schema_type": "choice123",
                    },
                },
            },
            "error: API schema type 'choice123' from file is not a valid options",
            "Expected error for lack of API schema type",
        ),
    ],
)
def test_targets_add__api_target_argument_from_file_validation(
    file_content,
    expected_error,
    assert_fail_msg,
    targets__add__sdk_add_target_mock: MagicMock,
    create_testable_yaml_file,
    probely_cli,
):
    testable_yaml_file_path: str = create_testable_yaml_file(file_content)

    stdout_lines, stderr_lines = probely_cli(
        "targets",
        "add",
        "-f",
        testable_yaml_file_path,
        return_list=True,
    )

    assert len(stdout_lines) == 0, "Expected no output, only errors"
    assert stderr_lines[-1] == "probely targets add: " + expected_error, assert_fail_msg
    assert targets__add__sdk_add_target_mock.call_count == 0


@pytest.fixture
def _valid_yaml_file_content() -> dict:
    valid_content = {
        "type": TargetTypeEnum.API.api_request_value,
        "site": {
            "name": "testable_target_name_from_file",
            "url": "https://testable_url_from_file.com",
            "api_scan_settings": {
                "api_schema_type": TargetAPISchemaTypeEnum.POSTMAN.api_request_value,
                "api_schema_url": "https://target_from_file.com/api_schema.json",
                "other_api_schema_property": "control_value",
            },
            "other_api_property": "control_value",
        },
        "other_api_property": "control_value",
    }
    return valid_content


@patch("probely.cli.commands.targets.add.add_target")
def test_targets_add__arguments_extracted_from_file_content(
    sdk_add_target_mock: MagicMock,
    create_testable_yaml_file,
    _valid_yaml_file_content,
    probely_cli,
):
    expected_id = "randoms123"
    sdk_add_target_mock.return_value = {"id": expected_id}

    testable_yaml_file_path: str = create_testable_yaml_file(_valid_yaml_file_content)
    stdout_l, stderr_l = probely_cli(
        "targets add",
        "-f",
        testable_yaml_file_path,
        return_list=True,
    )

    assert len(stderr_l) == 0, "Expected no errors"
    assert len(stdout_l) == 1, "Expected id of created target"
    assert stdout_l[0] == expected_id, "Expected id of created target"

    assert sdk_add_target_mock.call_count == 1, "Expected sdk add_target to be called"

    expected_arguments = {
        "target_url": _valid_yaml_file_content["site"]["url"],
        "target_name": _valid_yaml_file_content["site"]["name"],
        "target_type": TargetTypeEnum.get_by_api_response_value(
            _valid_yaml_file_content["type"]
        ),
        "api_schema_file_url": _valid_yaml_file_content["site"]["api_scan_settings"][
            "api_schema_url"
        ],
        "api_schema_type": TargetAPISchemaTypeEnum.get_by_api_response_value(
            _valid_yaml_file_content["site"]["api_scan_settings"]["api_schema_type"]
        ),
        "extra_payload": _valid_yaml_file_content,
    }

    _, mock_kwargs = sdk_add_target_mock.call_args
    assert mock_kwargs == expected_arguments, "Expected request with file content"


@patch("probely.cli.commands.targets.add.add_target")
def test_targets_add__command_arguments_override_file_content(
    sdk_add_target_mock: MagicMock,
    create_testable_yaml_file,
    _valid_yaml_file_content,
    probely_cli,
):
    expected_id = "randoms123"
    sdk_add_target_mock.return_value = {"id": expected_id}

    expected_url = "https://url_from_argument.com"
    expected_target_name = "name_from_argument"
    expected_target_type = "API"
    expected_api_schema_type = "OPENAPI"
    expected_api_schema_url = "www.api_schema_from_argument.com"
    testable_yaml_file_path: str = create_testable_yaml_file(_valid_yaml_file_content)

    stdout_l, stderr_l = probely_cli(
        "targets add",
        "--target-name",
        expected_target_name,
        "--target-type",
        expected_target_type,
        "--api-schema-type",
        expected_api_schema_type,
        "--api-schema-file-url",
        expected_api_schema_url,
        "--yaml-file",
        testable_yaml_file_path,
        "--",
        expected_url,
        return_list=True,
    )

    assert len(stderr_l) == 0, "Expected no errors"
    assert len(stdout_l) == 1, "Expected id of created target"
    assert stdout_l[0] == expected_id, "Expected id of created target"

    assert sdk_add_target_mock.call_count == 1, "Expected sdk add_target to be called"

    expected_arguments = {
        "target_url": expected_url,
        "target_name": expected_target_name,
        "target_type": TargetTypeEnum[expected_target_type],
        "api_schema_type": TargetAPISchemaTypeEnum[expected_api_schema_type],
        "api_schema_file_url": expected_api_schema_url,
        "extra_payload": _valid_yaml_file_content,
    }

    _, mock_kwargs = sdk_add_target_mock.call_args
    assert (
        mock_kwargs == expected_arguments
    ), "Expected sdk call with command args, overwriting --yaml-file input"


@patch("probely.cli.commands.targets.add.add_target")
def test_targets_add__output_argument_validation(_: MagicMock, probely_cli):
    stdout_lines, stderr_lines = probely_cli(
        "targets",
        "add",
        "-o",
        "random_text",
        return_list=True,
    )
    assert stdout_lines == []
    assert (
        stderr_lines[-1]
        == "probely targets add: error: argument -o/--output: invalid choice: "
        "'RANDOM_TEXT' (choose from 'YAML', 'JSON')"
    )


@patch("probely.cli.commands.targets.add.add_target")
def test_targets_add__output_argument_output(
    sdk_add_target_mock,
    valid_add_targets_api_response,
    probely_cli,
):
    sdk_add_target_mock.return_value = valid_add_targets_api_response

    stdout_lines, stderr_lines = probely_cli(
        "targets add http://www.random_url.com",
        "-o yaml",
    )

    assert stderr_lines == ""
    yaml_content = yaml.load(stdout_lines, Loader=yaml.FullLoader)
    assert isinstance(yaml_content, dict), "Expected a yaml object"
    assert (
        yaml_content["id"] == valid_add_targets_api_response["id"]
    ), "Expected sdk return in yaml content"

    stdout_lines, stderr_lines = probely_cli(
        "targets add http://www.random_url.com",
        "-o json",
    )

    assert stderr_lines == ""
    json_content = json.loads(stdout_lines)
    assert isinstance(json_content, dict), "Expected a json object"
    assert (
        json_content["id"] == valid_add_targets_api_response["id"]
    ), "Expected sdk return in json content"
