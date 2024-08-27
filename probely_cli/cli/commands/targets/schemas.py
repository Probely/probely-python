from typing import Type

import marshmallow
from marshmallow import Schema, post_load

from probely_cli.cli.common import TargetTypeEnum, TargetRiskEnum
from probely_cli.utils import ProbelyCLIEnum


class ProbelyCLIEnumField(marshmallow.fields.Enum):
    enum_class: Type[ProbelyCLIEnum]

    def __init__(self, enum_class: Type[ProbelyCLIEnum], *args, **kwargs):
        self.enum_class = enum_class
        super().__init__(enum=enum_class, *args, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        raise NotImplementedError()

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return self.enum_class[value].api_filter_value
        except:
            raise marshmallow.ValidationError("Values not within the accepted values.")


class TargetApiFiltersSchema(Schema):
    unlimited = marshmallow.fields.Boolean(
        required=False,
        allow_none=True,
        data_key="f_has_unlimited_scans",
    )
    verified = marshmallow.fields.Boolean(
        required=False,
        allow_none=True,
        data_key="f_is_url_verified",
    )
    risk = marshmallow.fields.List(
        ProbelyCLIEnumField(TargetRiskEnum),
        required=False,
        allow_none=True,
        data_key="f_risk",
    )

    type = marshmallow.fields.List(
        ProbelyCLIEnumField(TargetTypeEnum),
        required=False,
        allow_none=True,
        data_key="f_type",
    )

    search = marshmallow.fields.Str(
        required=False,
        allow_none=True,
        data_key="f_search",
    )

    @post_load
    def ignore_unused_filters(self, data, **kwargs):
        command_filters = {f: v for f, v in data.items() if v is not None}
        return command_filters

    class Meta:
        unknown = marshmallow.EXCLUDE
