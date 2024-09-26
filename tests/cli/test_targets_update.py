import json
from unittest.mock import patch

import pytest
import yaml

from tests.testable_api_responses import RETRIEVE_TARGET_200_RESPONSE


@pytest.mark.parametrize(
    "args, expected_error",
    [
        (
            ["targets", "update", "target_id1"],
            "probely targets update: error: Path to the YAML file that contains the payload is required.",
        ),
        (
            [
                "targets",
                "update",
                "target_id1 target_id2",
                "-f update_payload.yaml",
                "--f-has-unlimited-scans=True",
            ],
            "probely targets update: error: filters and Target IDs are mutually exclusive.",
        ),
        (
            ["targets", "update", "-f update_payload.yaml"],
            "probely targets update: error: either filters or Target IDs must be provided.",
        ),
    ],
)
@patch("probely_cli.cli.commands.targets.update.validate_and_retrieve_yaml_content")
def test_targets_update__validation(
    get_yaml_file_content_mock, probely_cli, args, expected_error
):
    """
    Validate the target update command:
    - Requires a path to the YAML file.
    - Filters and Target IDs are mutually exclusive.
    - Either filters or Target IDs must be provided.
    """
    get_yaml_file_content_mock.return_value = {"name": "Updated name"}

    stdout_lines, stderr_lines = probely_cli(*args, return_list=True)

    assert len(stdout_lines) == 0, f"Expected no output, but got: {stdout_lines}"
    assert len(stderr_lines) == 1, f"Expected error output, but got: {stderr_lines}"

    assert (
        stderr_lines[0] == expected_error
    ), f"Unexpected error message: {stderr_lines[0]}"


@patch("probely_cli.cli.commands.targets.update.update_target")
@patch("probely_cli.cli.commands.targets.update.validate_and_retrieve_yaml_content")
def test_target_update__output_format(
    get_yaml_file_content_mock,
    update_targets_mock,
    probely_cli,
):
    """
    Test the output format of the target update command.
    """
    target_update_payload = {
        "name": "Updated name",
    }
    get_yaml_file_content_mock.return_value = target_update_payload

    target_id = "target_id1"
    updated_target_content = RETRIEVE_TARGET_200_RESPONSE.copy()
    updated_target_content["id"] = target_id
    updated_target_content["site"]["name"] = target_update_payload["name"]

    update_targets_mock.return_value = updated_target_content

    # Case 1: JSON output
    stdout, stderr = probely_cli(
        "targets",
        "update",
        target_id,
        "-f update_payload.yaml",
        "--output json",
    )
    assert stderr == ""
    json_content = json.loads(stdout)
    assert isinstance(json_content, list), "Expected a json list"
    assert len(json_content) == 1  # Only one target which was updated
    assert json_content[0]["id"] == target_id
    assert json_content[0]["site"]["name"] == target_update_payload["name"]

    # Case 2: YAML output
    stdout, stderr = probely_cli(
        "targets",
        "update",
        target_id,
        "-f update_payload.yaml",
        "-o yaml",
    )
    assert stderr == ""
    yaml_content = yaml.load(stdout, Loader=yaml.FullLoader)
    assert yaml_content[0]["id"] == target_id
    assert yaml_content[0]["site"]["name"] == target_update_payload["name"]

    # Case 3 - No output format specified, only target IDs should be printed
    stdout, stderr = probely_cli(
        "targets",
        "update",
        target_id,
        "-f update_payload.yaml",
    )
    assert stdout == f"{target_id}\n", stdout


@patch("probely_cli.cli.commands.targets.update.update_target")
@patch("probely_cli.cli.commands.targets.update.update_targets")
@patch("probely_cli.cli.commands.targets.update.validate_and_retrieve_yaml_content")
def test_targets_update__calls_correct_sdk_function(
    get_yaml_file_content_mock,
    sdk_update_targets_mock,
    sdk_update_target_mock,
    probely_cli,
):
    """
    Ensure that correct SDK function is called based on the number of Target IDs provided.

    - If a single target ID is provided, `update_target()` should be called.
    - If multiple target IDs are provided, `update_targets()` should be called.
    """
    update_payload = {"name": "Updated name"}
    get_yaml_file_content_mock.return_value = update_payload

    # Test case 1: Single target ID
    probely_cli("targets", "update", "target_id1", "-f update_payload.yaml")
    sdk_update_target_mock.assert_called_once_with("target_id1", update_payload)
    sdk_update_targets_mock.assert_not_called()

    sdk_update_target_mock.reset_mock()
    sdk_update_targets_mock.reset_mock()

    # Test case 2: Multiple Target IDs
    probely_cli(
        "targets", "update", "target_id1", "target_id2", "-f update_payload.yaml"
    )
    sdk_update_targets_mock.assert_called_once_with(
        ["target_id1", "target_id2"], update_payload
    )
    sdk_update_target_mock.assert_not_called()


@pytest.mark.parametrize(
    "filtered_targets",
    [
        ([{"id": "target_id1"}]),
        ([{"id": "target_id1"}, {"id": "target_id2"}]),
    ],
)
@patch("probely_cli.cli.commands.targets.update.list_targets")
@patch("probely_cli.cli.commands.targets.update.update_target")
@patch("probely_cli.cli.commands.targets.update.update_targets")
@patch("probely_cli.cli.commands.targets.update.validate_and_retrieve_yaml_content")
def test_targets_update__with_filters(
    get_yaml_file_content_mock,
    update_targets_mock,
    update_target_mock,
    list_targets_mock,
    probely_cli,
    filtered_targets,
):
    update_payload = {"name": "Updated name"}
    get_yaml_file_content_mock.return_value = update_payload
    list_targets_mock.return_value = filtered_targets

    _, stderr = probely_cli(
        "targets",
        "update",
        "-f update_payload.yaml",
        "--f-has-unlimited-scans=True",
        "--f-is-url-verified=False",
        return_list=True,
    )

    assert len(stderr) == 0, f"Expected no errors, but got: {stderr}"
    list_targets_mock.assert_called_once_with(
        targets_filters={"unlimited": True, "verified": False}
    )

    target_ids = [target["id"] for target in filtered_targets]

    if len(target_ids) == 1:
        update_target_mock.assert_called_once_with(target_ids[0], update_payload)
    else:
        update_targets_mock.assert_called_once_with(target_ids, update_payload)
