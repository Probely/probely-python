class ProbelyException(Exception):
    pass


class ProbelyRequestFailed(ProbelyException):
    pass


class ProbelyBadRequest(ProbelyException):
    def __init__(self, *args, **kwargs):
        super().__init__("API Validation Error.", *args)
        self.response_payload = kwargs.get("response_payload")


class ProbelyMissConfig(ProbelyException):
    pass


class ProbelyCLIValidation(ProbelyException):
    pass


class ProbelyApiUnavailable(ProbelyException):
    def __init__(self, *args, **kwargs):
        super().__init__("API is unavailable. Contact support.", *args, **kwargs)
