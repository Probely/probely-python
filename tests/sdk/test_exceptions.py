from probely_cli.exceptions import ProbelyObjectNotFound, ProbelyRequestFailed


def test_probely_object_not_found_exception():
    random_id = "random_id"
    exc = ProbelyObjectNotFound(id=random_id)

    assert exc.not_found_object_id == random_id
    assert str(exc) == "object '" + random_id + "' not found."


def test_probely_request_failed_exception():
    testable_reason = "random text reason"
    exc = ProbelyRequestFailed(reason=testable_reason)

    assert exc.reason == testable_reason
    assert str(exc) == testable_reason
