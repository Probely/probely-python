import pytest

from probely_cli.cli.formatters import get_printable_enum_value, UNKNOWN_VALUE_REP
from probely_cli.utils import ProbelyCLIEnum


class TestableEnum(ProbelyCLIEnum):
    A = ("api_resp_A", "api_filters_A")


@pytest.mark.parametrize(
    "value, expected",
    [
        (TestableEnum.A.api_response_value, TestableEnum.A.name),
        (TestableEnum.A.api_filter_value, UNKNOWN_VALUE_REP),
        ("random", UNKNOWN_VALUE_REP),
    ],
)
def test_get_printable_enum_value(value, expected):
    printable_value = get_printable_enum_value(TestableEnum, value)
    assert printable_value == expected
