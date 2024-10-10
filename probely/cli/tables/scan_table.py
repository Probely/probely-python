from rich.table import Table

from probely.cli.renderers import get_printable_date, get_printable_labels
from probely.cli.tables.base_table import BaseOutputTable


class ScanTable(BaseOutputTable):
    @classmethod
    def create_table(cls, show_header: bool = False) -> Table:
        table = Table(show_header=show_header, box=None)

        table.add_column("ID", width=12)
        table.add_column("NAME", width=36, no_wrap=True)
        table.add_column("URL", width=48, no_wrap=True)
        table.add_column("STATUS", width=12, no_wrap=True)
        table.add_column("START_DATE", width=16)
        table.add_column("HIGHS", width=5)
        table.add_column("MEDIUMS", width=7)
        table.add_column("LOWS", width=4)
        table.add_column("LABELS", width=16, no_wrap=True)

        return table

    @classmethod
    def add_row(cls, table: Table, scan: dict) -> None:
        target = scan.get("target", {})
        site = target.get("site", {})

        table.add_row(
            scan.get("id"),
            site.get("name", "N/D"),
            site.get("url"),
            scan["status"],
            get_printable_date(scan["started"]),
            str(scan["highs"]),
            str(scan["mediums"]),
            str(scan["lows"]),
            get_printable_labels(target["labels"]),
        )
