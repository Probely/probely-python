from typing import Dict

from rich.table import Table
from probely_cli.cli.renderers import (
    get_printable_enum_value,
    get_printable_labels,
    get_printable_last_scan_date,
)
from probely_cli.cli.tables.base_table import BaseOutputTable
from probely_cli.sdk.enums import TargetRiskEnum


class TargetTable(BaseOutputTable):
    def create_table(self, show_header: bool = False) -> Table:
        table = Table(show_header=show_header, box=None)

        table.add_column("ID", width=12)
        table.add_column("NAME", width=36, no_wrap=True)
        table.add_column("URL", width=48, no_wrap=True)
        table.add_column("RISK", width=7)
        table.add_column("LAST_SCAN", width=16)
        table.add_column("LABELS", width=16, no_wrap=True)

        return table

    def add_row(self, table: Table, target: Dict) -> None:
        site = target.get("site")

        table.add_row(
            target.get("id"),
            site.get("name", "N/D"),
            site.get("url"),
            get_printable_enum_value(TargetRiskEnum, target["risk"]),
            get_printable_last_scan_date(target),
            get_printable_labels(target["labels"]),
        )
