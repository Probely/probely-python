from enum import Enum


class ProbelyCLIEnum(Enum):
    def __init__(self, api_response_value, api_filter_value=None):
        self._value_ = api_response_value
        self._api_filter_value = api_filter_value or api_response_value

    @property
    def api_filter_value(self):
        return self._api_filter_value

    @property
    def api_response_value(self):
        return self.value

    @classmethod
    def get_by_api_response_value(cls, value):
        for enum_element in cls:
            if enum_element.value == value:
                return enum_element

        raise ValueError("{} is not a valid {}".format(value, cls.__name__))

    @classmethod
    def get_by_api_filter_value(cls, api_filter_value):
        for enum_element in cls:
            if enum_element._api_filter_value == api_filter_value:
                return enum_element

        raise ValueError("{} is not a valid {}".format(api_filter_value, cls.__name__))
