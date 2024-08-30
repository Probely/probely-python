import marshmallow

from probely_cli.cli.common import (
    ProbelyCLIEnumField,
    FindingSeverityEnum,
    ProbelyCLIBaseFiltersSchema,
    FindingStateEnum,
)


class FindingsApiFiltersSchema(ProbelyCLIBaseFiltersSchema):
    scan = marshmallow.fields.List(
        marshmallow.fields.Str(),
        required=False,
        allow_none=True,
        data_key="f_scans",
    )
    severity = marshmallow.fields.List(
        ProbelyCLIEnumField(FindingSeverityEnum),
        required=False,
        allow_none=True,
        data_key="f_severity",
    )

    state = marshmallow.fields.List(
        ProbelyCLIEnumField(FindingStateEnum),
        required=False,
        allow_none=True,
        data_key="f_state",
    )

    target = marshmallow.fields.List(
        marshmallow.fields.Str(),
        required=False,
        allow_none=True,
        data_key="f_targets",
    )

    search = marshmallow.fields.Str(
        required=False,
        allow_none=True,
        data_key="f_search",
    )

    new = marshmallow.fields.Boolean(
        required=False,
        allow_none=True,
        data_key="f_is_new",
    )
