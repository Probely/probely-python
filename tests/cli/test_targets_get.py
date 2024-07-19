import re
from unittest.mock import patch, Mock


@patch("probely_cli.cli.commands.targets.get.get_targets")
def test_targets_get__table_headers_output(
    sdk_get_targets_mock: Mock,
    valid_get_targets_api_response: dict,
    probely_cli,
) -> None:
    sdk_get_targets_mock.return_value = valid_get_targets_api_response["results"]

    stdout, stderr = probely_cli("targets", "get")

    table_header = stdout[0]
    assert "ID" in table_header
    assert "NAME" in table_header
    assert "URL" in table_header
    assert "RISK" in table_header
    assert "LAST_SCAN" in table_header
    assert "LABELS" in table_header

    assert len(stderr) == 0


@patch("probely_cli.cli.commands.targets.get.get_targets")
def tests_targets_get__table_last_scan_date_output(
    sdk_get_targets_mock: Mock,
    probely_cli,
    valid_get_targets_api_response,
):
    testable_target_result = valid_get_targets_api_response["results"][0]
    sdk_get_targets_mock.return_value = [testable_target_result]

    stdout, stderr = probely_cli("targets", "get", return_list=True)

    column_separator = "  "  # double space

    table_header = stdout[0]
    table_columns = table_header.split()
    assert table_columns[4] == "LAST_SCAN"

    target_line = stdout[1]
    target_line = re.sub(r" {3,}", "  ", target_line)
    target_line = target_line.strip()
    target_columns = target_line.split(column_separator)
    assert target_columns[4] == "2024-07-15 15:07"
