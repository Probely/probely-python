from abc import ABC, abstractmethod

from rich.table import Table


class BaseOutputTable(ABC):
    @classmethod
    @abstractmethod
    def create_table(cls, show_header: bool) -> Table:
        """
        Initializes and returns a Rich Table with predefined columns.
        """
        pass

    @classmethod
    @abstractmethod
    def add_row(cls, table: Table, record: dict) -> None:
        """
        Adds a single row to the provided Rich Table based on the record data.
        """
        pass
