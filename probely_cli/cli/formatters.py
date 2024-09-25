import textwrap
from typing import Type, Dict, List, Union

from dateutil import parser

from probely_cli.utils import ProbelyCLIEnum

UNKNOWN_VALUE_REP = "UNKNOWN"


def get_printable_enum_value(enum: Type[ProbelyCLIEnum], api_enum_value: str) -> str:
    try:
        value_name: str = enum.get_by_api_response_value(api_enum_value).name
        return value_name
    except ValueError:
        return UNKNOWN_VALUE_REP  # TODO: scenario that risk enum updated but CLI is forgotten


def get_printable_labels(labels: List[Dict] = None) -> str:
    if labels is None:
        return "UNKNOWN_LABELS"

    labels_names = []
    try:
        for label in labels:
            truncated_label = textwrap.shorten(
                label["name"], width=16, placeholder="..."
            )
            labels_names.append(truncated_label)
    except:
        return "UNKNOWN_LABELS"

    printable_labels = ", ".join(labels_names)

    return printable_labels


def get_printable_date(
    date_string: Union[str, None],
    default_string: Union[str, None] = None,
) -> str:
    if date_string:
        datetime = parser.isoparse(date_string)
        return datetime.strftime("%Y-%m-%d %H:%M")

    if default_string:
        return default_string

    return ""
