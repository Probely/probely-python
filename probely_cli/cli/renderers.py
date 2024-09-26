import json
import sys
import textwrap
from typing import Dict, Generator, List, Optional, Type

from dateutil import parser
import yaml
from rich.console import Console
from rich.live import Live

from probely_cli.cli.enums import EntityTypeEnum, OutputEnum
from probely_cli.sdk.enums import ProbelyCLIEnum

from typing import Union


UNKNOWN_VALUE_REP = "UNKNOWN"


class OutputRenderer:
    """
    Class responsible for rendering output in various formats (JSON, YAML, Table).
    """

    def __init__(
        self,
        records: Generator[dict, None, None],
        output_type: Optional[OutputEnum],
        console: Console,
        entity_type: EntityTypeEnum,
    ):
        self.records = records
        self.output_type = output_type
        self.console = console
        self.entity_type = entity_type

    def render(self) -> None:
        if self.output_type == OutputEnum.JSON:
            self._render_json()
        elif self.output_type == OutputEnum.YAML:
            self._render_yaml()
        else:
            self._render_table()

    def _render_json(self) -> None:
        self.console.print("[")
        first = True
        for record in self.records:
            if not first:
                self.console.print(",")
            self.console.print(json.dumps(record, indent=2))
            first = False
        self.console.print("]")

    def _render_yaml(self) -> None:
        for record in self.records:
            self.console.print(yaml.dump([record], indent=2, width=sys.maxsize))

    def _render_table(self) -> None:
        from probely_cli.cli.tables.table_factory import (
            TableFactory,
        )  # Avoid circular import

        table_cls = TableFactory.get_table_class(self.entity_type)
        table = table_cls().create_table(show_header=True)
        with Live(table, console=self.console):
            for record in self.records:
                table_cls().add_row(table, record)


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
