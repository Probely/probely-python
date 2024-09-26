from probely_cli.sdk.enums import ProbelyCLIEnum


def test_probely_cli_enum():
    a_value_from_api_response = "a"
    a_value_for_api_call = "a_api"

    class AEnum(ProbelyCLIEnum):
        A = (a_value_from_api_response, a_value_for_api_call)

    assert (
        AEnum.A.value == a_value_from_api_response
    ), "Expected value to point to value the api responds"
    assert (
        AEnum.A.api_response_value == a_value_from_api_response
    ), "Expected api_response_value to point to value the api responds"
    assert (
        AEnum.A.api_filter_value == a_value_for_api_call
    ), "Expected api_filter_value to point to value to be used in api filter call"

    assert (
        AEnum.get_by_api_response_value(a_value_from_api_response) == AEnum.A
    ), "Expected to be able to retrieve Enum instance with values listed as api responses"
    assert (
        AEnum.get_by_api_filter_value(a_value_for_api_call) == AEnum.A
    ), "Expected to be able to retrieve Enum instance with values listed as api filters"

    b_value = "a"

    class BEnum(ProbelyCLIEnum):
        B = b_value

    assert BEnum.B.value == b_value
    assert BEnum.B.api_response_value == b_value
    assert (
        BEnum.B.api_filter_value == b_value
    ), "Expected when custom value for api filter is missing, normal value is used"
