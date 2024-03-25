import json
from typing import List

import probely_cli

from probely_cli.exceptions import ProbelyRequestFailed

if __name__ == "__main__":

    # You can config programmatically
    # probely_cli.Probely.init(api_key="add api_key here")

    targets_list: List[object] = []

    try:
        targets_list = probely_cli.list_targets()
    except ProbelyRequestFailed as probely_exception:
        print("Probely sdk error:", probely_exception)

    for target in targets_list:
        print(json.dumps(target, indent=4))
