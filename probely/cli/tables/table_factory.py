from typing import Type

from probely.cli.enums import EntityTypeEnum
from probely.cli.tables.base_table import BaseOutputTable
from probely.cli.tables.finding_table import FindingTable
from probely.cli.tables.scan_table import ScanTable
from probely.cli.tables.targets_table import TargetTable


class TableFactory:
    @staticmethod
    def get_table_class(entity_type: EntityTypeEnum) -> Type[BaseOutputTable]:
        ENTITY_TABLE_MAPPING = {
            EntityTypeEnum.FINDING: FindingTable,
            EntityTypeEnum.SCAN: ScanTable,
            EntityTypeEnum.TARGET: TargetTable,
        }

        return ENTITY_TABLE_MAPPING[entity_type]
