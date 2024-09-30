class ProbelyException(Exception):
    pass


class ProbelyRequestFailed(ProbelyException):
    """General exception for non successful api calls"""

    def __init__(self, reason, *args, **kwargs):
        super().__init__(reason, *args)
        self.reason = reason


class ProbelyObjectNotFound(ProbelyException):
    def __init__(self, id, *args, **kwargs):
        super().__init__("object '{}' not found.".format(id), *args)
        self.not_found_object_id = id


class ProbelyBadRequest(ProbelyException):
    def __init__(self, response_payload, *args, **kwargs):
        super().__init__("API validation error: {}".format(response_payload), *args)
        self.response_payload = response_payload


class ProbelyMissConfig(ProbelyException):
    pass


class ProbelyCLIValidation(ProbelyException):
    pass


class ProbelyApiUnavailable(ProbelyException):
    def __init__(self, *args, **kwargs):
        super().__init__("API is unavailable. Contact support.", *args, **kwargs)
