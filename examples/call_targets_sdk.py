import json
from typing import List

from probely_cli import Probely, ProbelyException, list_targets

if __name__ == "__main__":

    Probely.init(api_key="your_api_key")

    try:
        targets_list: List[dict] = list_targets()

        for target in targets_list:
            print(json.dumps(target, indent=4))

    except ProbelyException as probely_exception:
        print("Probely sdk error:", probely_exception)
