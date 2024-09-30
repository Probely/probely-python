from typing import Type

import dateutil
import marshmallow

from probely.sdk.enums import ProbelyCLIEnum


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


class ISO8601DateTimeField(marshmallow.fields.Field):
    """
    Field for parsing ISO 8601 datetime strings into datetime objects and serializing them back.

    An ISO-8601 datetime string consists of a date portion, followed optionally by a time
    portion - the date and time portions are separated by a single character separator,
    which is ``T`` in the official standard.

    Supported common date formats are:
    - ``YYYY``
    - ``YYYY-MM``
    - ``YYYY-MM-DD`` or ``YYYYMMDD``

    Supported common time formats are:
    - ``hh``
    - ``hh:mm`` or ``hhmm``
    - ``hh:mm:ss`` or ``hhmmss``
    - ``hh:mm:ss.ssssss`` (Up to 6 sub-second digits)
    """

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return dateutil.parser.isoparse(value)
        except (ValueError, TypeError, OverflowError):
            raise marshmallow.ValidationError(
                "Invalid datetime format. Please provide a valid datet##ime in ISO 8601 format."
            )

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.isoformat()
