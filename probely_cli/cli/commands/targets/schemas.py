import marshmallow

from probely_cli.cli.common import (
    ProbelyCLIEnumField,
    ProbelyCLIBaseFiltersSchema,
)
from probely_cli.sdk.common import TargetRiskEnum, TargetTypeEnum


class TargetApiFiltersSchema(ProbelyCLIBaseFiltersSchema):
    unlimited = marshmallow.fields.Boolean(
        allow_none=True,
        data_key="f_has_unlimited_scans",
    )
    verified = marshmallow.fields.Boolean(
        allow_none=True,
        data_key="f_is_url_verified",
    )
    risk = marshmallow.fields.List(
        ProbelyCLIEnumField(TargetRiskEnum),
        allow_none=True,
        data_key="f_risk",
    )
    type = marshmallow.fields.List(
        ProbelyCLIEnumField(TargetTypeEnum),
        allow_none=True,
        data_key="f_type",
    )
    search = marshmallow.fields.Str(
        allow_none=True,
        data_key="f_search",
    )
