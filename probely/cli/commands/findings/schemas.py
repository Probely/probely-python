import marshmallow

from probely.cli.schemas.base_schema import ProbelyCLIBaseFiltersSchema
from probely.cli.schemas.custom_fields import ProbelyCLIEnumField
from probely.sdk.enums import FindingSeverityEnum, FindingStateEnum


class FindingsApiFiltersSchema(ProbelyCLIBaseFiltersSchema):
    scan = marshmallow.fields.List(
        marshmallow.fields.Str(),
        allow_none=True,
        data_key="f_scans",
    )
    severity = marshmallow.fields.List(
        ProbelyCLIEnumField(FindingSeverityEnum),
        allow_none=True,
        data_key="f_severity",
    )

    state = marshmallow.fields.List(
        ProbelyCLIEnumField(FindingStateEnum),
        allow_none=True,
        data_key="f_state",
    )

    target = marshmallow.fields.List(
        marshmallow.fields.Str(),
        allow_none=True,
        data_key="f_targets",
    )

    search = marshmallow.fields.Str(
        allow_none=True,
        data_key="f_search",
    )

    new = marshmallow.fields.Boolean(
        allow_none=True,
        data_key="f_is_new",
    )
