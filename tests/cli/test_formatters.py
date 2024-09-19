import pytest

from probely_cli.cli.formatters import get_printable_enum_value, UNKNOWN_VALUE_REP
from probely_cli.utils import ProbelyCLIEnum


class EnumTestable(ProbelyCLIEnum):
    A = ("api_resp_A", "api_filters_A")


@pytest.mark.parametrize(
    "value, expected",
    [
        (EnumTestable.A.api_response_value, EnumTestable.A.name),
        (EnumTestable.A.api_filter_value, UNKNOWN_VALUE_REP),
        ("random", UNKNOWN_VALUE_REP),
    ],
)
def test_get_printable_enum_value(value, expected):
    printable_value = get_printable_enum_value(EnumTestable, value)
    assert printable_value == expected
