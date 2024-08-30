import marshmallow

from probely_cli.cli.common import (
    TargetTypeEnum,
    TargetRiskEnum,
    ProbelyCLIEnumField,
    ProbelyCLIBaseFiltersSchema,
)


class TargetApiFiltersSchema(ProbelyCLIBaseFiltersSchema):
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
