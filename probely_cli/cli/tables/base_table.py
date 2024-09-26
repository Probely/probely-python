from abc import ABC, abstractmethod

from rich.table import Table


class BaseOutputTable(ABC):
    @abstractmethod
    def create_table(self, show_header: bool) -> Table:
        """
        Initializes and returns a Rich Table with predefined columns.
        """
        pass

    @abstractmethod
    def add_row(self, table: Table, record: dict) -> None:
        """
        Adds a single row to the provided Rich Table based on the record data.
        """
        pass
