import marshmallow
from probely_cli.cli.common import (
    ISO8601DateTimeField,
    ProbelyCLIBaseFiltersSchema,
    ProbelyCLIEnumField,
    ScanStatusEnum,
)


class ScanApiFiltersSchema(ProbelyCLIBaseFiltersSchema):
    search = marshmallow.fields.Str(
        allow_none=True,
        data_key="f_search",
    )
    status = marshmallow.fields.List(
        ProbelyCLIEnumField(ScanStatusEnum), allow_none=True, data_key="f_status"
    )
    completed__gt = ISO8601DateTimeField(
        allow_none=True,
        data_key="f_completed_gt",
    )
    completed__gte = ISO8601DateTimeField(
        allow_none=True,
        data_key="f_completed_gte",
    )
    completed__lt = ISO8601DateTimeField(
        allow_none=True,
        data_key="f_completed_lt",
    )
    completed__lte = ISO8601DateTimeField(
        allow_none=True,
        data_key="f_completed_lte",
    )
    started__gt = ISO8601DateTimeField(
        allow_none=True,
        data_key="f_started_gt",
    )
    started__gte = ISO8601DateTimeField(
        allow_none=True,
        data_key="f_started_gte",
    )
    started__lt = ISO8601DateTimeField(
        allow_none=True,
        data_key="f_started_lt",
    )
    started__lte = ISO8601DateTimeField(
        allow_none=True,
        data_key="f_started_lte",
    )
