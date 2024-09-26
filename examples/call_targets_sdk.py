import json
from typing import List

from probely_cli import Probely, list_targets
from probely_cli.exceptions import ProbelyException

if __name__ == "__main__":

    # You can config programmatically
    Probely.init(api_key="your_api_key")

    try:
        targets_list: List[dict] = list_targets()

        for target in targets_list:
            print(json.dumps(target, indent=4))

    except ProbelyException as probely_exception:
        print("Probely sdk error:", probely_exception)
