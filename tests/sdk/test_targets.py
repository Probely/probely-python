import json
from unittest import mock
from probely_cli.sdk.targets import list_targets


# mock_client


@mock.patch("probely_cli.sdk.client.requests.Session.get")
def test_list_targets(mock_session):
    response_content = [{"list": "of objects1"}, {"list": "of objects2"}]
    expected_content = str.encode(json.dumps({"results": response_content}))

    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.content = expected_content

    mock_session.return_value = mock_response

    r = list_targets()
    assert r == response_content
