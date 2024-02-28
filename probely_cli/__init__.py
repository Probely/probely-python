from .config import init, probely_client
from .exceptions import *
from .targets import list_targets

__all__ = [
    # defines behaviour of "from probely_cli import *"
    # TODO: seems to be a good practice
]


def hello():
    return "Hello from probely-cli!"
