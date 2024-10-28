from ._schemas import Finding as FindingDataModel


class SdkBaseModel:
    """
    Base class for all resource models, providing common serialization methods.
    """

    serializer_class = None  # To be defined in subclasses

    def __init__(self, data_model):
        self._data = data_model

    def __getattr__(self, name):
        return getattr(self._data, name)

    def to_dict(self, *args, **kwargs) -> dict:
        """
        Serialize the object to a dictionary.
        """
        return self._data.model_dump(*args, **kwargs)

    def to_json(self, *args, **kwargs) -> str:
        """
        Serialize the object to a JSON string.
        """
        return self._data.model_dump_json(*args, **kwargs)


class Finding(SdkBaseModel):
    serializer_class = FindingDataModel

    def __init__(self, data_model: FindingDataModel):
        super().__init__(data_model)
