import json

from probely import Probely, ProbelyException, list_targets
from probely.exceptions import ProbelyRequestFailed

if __name__ == "__main__":

    Probely.init(api_key="your_api_key")

    try:
        targets_generator = list_targets()
        for target in targets_generator():
            print(json.dumps(target, indent=4))
    except ProbelyRequestFailed as request_error:
        print("Request to Probely API failed:", request_error)
    except ProbelyException as probely_exception:
        print("Probely SDK error:", probely_exception)
    except Exception as general_error:
        print("An unexpected error occurred:", general_error)
