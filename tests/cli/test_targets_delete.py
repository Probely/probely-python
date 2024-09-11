from unittest.mock import patch, Mock


@patch("probely_cli.cli.commands.targets.delete.delete_targets")
@patch("probely_cli.cli.commands.targets.delete.list_targets")
def test_targets_delete_target(
    list_targets_mock: Mock, delete_targets_mock: Mock, probely_cli
):
    target_id1 = "target_id1"
    target_id2 = "target_id2"

    delete_targets_mock.return_value = {"ids": [target_id1, target_id2]}

    stdout_lines, stderr_lines = probely_cli(
        "targets",
        "delete",
        target_id1,
        target_id2,
        return_list=True,
    )
    list_targets_mock.assert_not_called()
    delete_targets_mock.assert_called_once_with(targets_ids=[target_id1, target_id2])
    assert len(stderr_lines) == 0
    assert len(stdout_lines) == 2, "Expected to have 2 line with the deleted target id"
    assert target_id2 == stdout_lines[1]


@patch("probely_cli.cli.commands.targets.delete.delete_targets")
@patch("probely_cli.cli.commands.targets.delete.list_targets")
def test_targets_delete_target_with_filters(
    list_targets_mock: Mock, delete_targets_mock: Mock, probely_cli
):
    target_id1 = "target_id1"
    list_targets_mock.return_value = [{"id": target_id1}]

    delete_targets_mock.return_value = {"ids": [target_id1]}

    stdout_lines, stderr_lines = probely_cli(
        "targets",
        "delete",
        "--f-has-unlimited-scans=True",
        return_list=True,
    )

    list_targets_mock.assert_called_with(targets_filters={"unlimited": True})
    delete_targets_mock.assert_called_once_with(targets_ids=[target_id1])
    assert len(stderr_lines) == 0
    assert len(stdout_lines) == 1, "Expected to have 1 line with the deleted target id"
    assert target_id1 == stdout_lines[0]


def test_targets_delete__mutually_exclusive_arguments(probely_cli):
    stdout_lines, stderr_lines = probely_cli(
        "targets",
        "delete",
        "target_id1 target_id2",
        "--f-has-unlimited-scans=True",
        return_list=True,
    )

    assert len(stdout_lines) == 0, "Expected no output"
    assert len(stderr_lines) == 1, "Expected error output"

    assert stderr_lines[0] == (
        "probely targets delete: error: filters and Target IDs are mutually exclusive."
    )
