from functools import wraps

from rich.console import Console

err_console = Console(stderr=True)


class ProbelyException(Exception):
    pass


class ProbelyRequestFailed(ProbelyException):
    pass


def cli_exception_handler(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ProbelyException as e:
            err_console.print(e)

    return func_wrapper
