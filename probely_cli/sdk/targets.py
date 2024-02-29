import json

from ..config import probely_client
from ..exceptions import ProbelyRequestFailed
from ..settings import PROBELY_API_TARGETS_URL


def list_targets():
    # TODO: pagination
    # or maybe the option to return a generator for the sdk??
    r = probely_client.get(PROBELY_API_TARGETS_URL)

    output = json.loads(r.content)

    if r.status_code != 200:
        raise ProbelyRequestFailed(output["detail"])

    return output["results"]
