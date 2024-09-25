from unittest.mock import patch, Mock, MagicMock


@patch("probely_cli.cli.commands.targets.delete.delete_target")
@patch("probely_cli.cli.commands.targets.delete.delete_targets")
@patch("probely_cli.cli.commands.targets.delete.list_targets")
def test_targets_delete__multiple_targets(
    list_targets_mock: Mock,
    delete_targets_mock: Mock,
    delete_target_mock: MagicMock,
    probely_cli,
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

    assert delete_target_mock.call_count == 0, "Expected bulk call for multiple targets"
    assert list_targets_mock.call_count == 0, "Expected no search for multiple IDs"

    delete_targets_mock.assert_called_once_with(targets_ids=[target_id1, target_id2])
    assert stderr_lines == []
    assert len(stdout_lines) == 2, "Expected to have 2 line with the deleted target id"
    assert target_id1 == stdout_lines[0]
    assert target_id2 == stdout_lines[1]


@patch("probely_cli.cli.commands.targets.delete.delete_targets")
@patch("probely_cli.cli.commands.targets.delete.delete_target")
@patch("probely_cli.cli.commands.targets.delete.list_targets")
def test_targets_delete__one_target(
    list_targets_mock: Mock,
    delete_target_mock: MagicMock,
    delete_targets_mock: MagicMock,
    probely_cli,
):
    testable_target_id = "testable_target_id"
    delete_target_mock.return_value = testable_target_id

    stdout_lines, stderr_lines = probely_cli(
        "targets", "delete", testable_target_id, return_list=True
    )

    assert delete_targets_mock.call_count == 0, "Expected bulk delete to NOT called"
    assert list_targets_mock.call_count == 0, "Expected no search for ID"

    assert delete_target_mock.call_count == 1, "Expected usage of single delete"

    assert stderr_lines == []
    assert stdout_lines[-1] == testable_target_id


@patch("probely_cli.cli.commands.targets.delete.delete_target")
@patch("probely_cli.cli.commands.targets.delete.delete_targets")
@patch("probely_cli.cli.commands.targets.delete.list_targets")
def test_targets_delete__filters_with_multiple_results(
    list_targets_mock: Mock,
    delete_targets_mock: Mock,
    delete_target_mock: Mock,
    probely_cli,
):
    target_id1 = "target_id1"
    target_id2 = "target_id2"
    list_targets_mock.return_value = [{"id": target_id1}, {"id": target_id2}]

    delete_targets_mock.return_value = {"ids": [target_id1, target_id2]}

    stdout_lines, stderr_lines = probely_cli(
        "targets",
        "delete",
        "--f-has-unlimited-scans=True",
        return_list=True,
    )

    assert delete_target_mock.call_count == 0, "Expect single delete method not called"

    list_targets_mock.assert_called_with(targets_filters={"unlimited": True})
    delete_targets_mock.assert_called_once_with(targets_ids=[target_id1, target_id2])
    assert stderr_lines == []
    assert len(stdout_lines) == 2, "Expected to have 1 line with the deleted target id"
    assert target_id1 == stdout_lines[0]
    assert target_id2 == stdout_lines[1]


@patch("probely_cli.cli.commands.targets.delete.delete_target")
@patch("probely_cli.cli.commands.targets.delete.delete_targets")
@patch("probely_cli.cli.commands.targets.delete.list_targets")
def test_targets_delete__filters_with_single_result(
    list_targets_mock: Mock,
    delete_targets_mock: Mock,
    delete_target_mock: Mock,
    probely_cli,
):
    target_id1 = "target_id1"
    list_targets_mock.return_value = [{"id": target_id1}]

    delete_target_mock.return_value = target_id1

    stdout_lines, stderr_lines = probely_cli(
        "targets",
        "delete",
        "--f-has-unlimited-scans=True",
        return_list=True,
    )

    assert delete_targets_mock.call_count == 0, "Expect single delete method not called"

    list_targets_mock.assert_called_with(targets_filters={"unlimited": True})
    delete_target_mock.assert_called_once_with(target_id1)
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


@patch("probely_cli.cli.commands.targets.delete.delete_target")
@patch("probely_cli.cli.commands.targets.delete.delete_targets")
def test_targets_delete__without_any_argument(
    delete_targets_mock: Mock,
    delete_target_mock: Mock,
    probely_cli,
):
    stdout_lines, stderr_lines = probely_cli(
        "targets",
        "delete",
        return_list=True,
    )
    assert len(stdout_lines) == 0, "Expected no output"
    assert len(stderr_lines) == 1, "Expected error output"

    assert stderr_lines[-1] == (
        "probely targets delete: error: Expected target_ids or filters"
    )

    delete_targets_mock.assert_not_called()
    delete_target_mock.assert_not_called()
