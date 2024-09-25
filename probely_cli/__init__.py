from .sdk.client import Probely
from .sdk.targets import (
    list_targets,
    retrieve_target,
    retrieve_targets,
    delete_targets,
    add_target,
    update_target,
    update_targets,
)
from .version import __version__

__all__ = [
    "Probely",
    "add_target",
    "list_targets",
    "retrieve_target",
    "retrieve_targets",
    # "delete_target",
    "delete_targets",
    "update_target",
    "update_targets",
]
