from typing import Type

from probely_cli.cli.enums import EntityTypeEnum
from probely_cli.cli.tables.base_table import BaseOutputTable
from probely_cli.cli.tables.finding_table import FindingTable
from probely_cli.cli.tables.scan_table import ScanTable
from probely_cli.cli.tables.targets_table import TargetTable


class TableFactory:
    @staticmethod
    def get_table_class(entity_type: EntityTypeEnum) -> Type[BaseOutputTable]:
        ENTITY_TABLE_MAPPING = {
            EntityTypeEnum.FINDING: FindingTable,
            EntityTypeEnum.SCAN: ScanTable,
            EntityTypeEnum.TARGET: TargetTable,
        }

        return ENTITY_TABLE_MAPPING[entity_type]
