# Licensed under the MIT License.
# pylogop Copyright (C) 2023 numlinka.

# internal
from . import utils
from . import typeins
from . import constants
from . import exceptions

from ._ease import *
from .base import BaseLogging, BaseOutputStream
from .stream import StandardOutputStream, StandardOutputStreamPlus, FileOutputStream
from .logging import Logging
from .decorators import callabletrack


__name__ = "logop"
__author__ = "numlinka"
__license__ = "LGPL 3.0"
__copyright__ = "Copyright (C) 2023 numlinka"

__version_info__ = (1, 3, 0)
__version__ = ".".join(map(str, __version_info__))


# ! __all__ is not declared for `ease`, so you can't import it via `from _ import *`.
__all__ = [
    "Logging",
    "StandardOutputStream",
    "StandardOutputStreamPlus",
    "FileOutputStream",
    "BaseLogging",
    "BaseOutputStream",
    "utils",
    "typeins",
    "constants",
    "exceptions",
    "callabletrack"
]
