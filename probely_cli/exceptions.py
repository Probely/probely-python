class ProbelyException(Exception):
    pass


class ProbelyRequestFailed(ProbelyException):
    pass


class ProbelyMissConfig(ProbelyException):
    pass
