# Licensed under the MIT License.
# logop by numlinka.

# self
from .utils import *
from .levels import *
from .formats import *
from .decorators import *
from .exceptions import *

from .logging_base import *
from .logging_main import *

from .logoutput_base import *
from .logoutput_std import *
from .logoutput_stdplus import *
from .logoutput_file import *


__name__ = "logop"
__author__ = "numlinka"
__license__ = "LGPL 3.0"
__copyright__ = "Copyright (C) 2023 numlinka"

__version_info__ = (1, 2, 4)
__version__ = ".".join(map(str, __version_info__))


__all__ = [
    "ALL",
    "TRACE",
    "DEBUG",
    "INFO",
    "WARN",
    "WARNING",
    "SEVERE",
    "ERROR",
    "CRITICAL",
    "FATAL",
    "OFF",

    "TRACE_NAME",
    "DEBUG_NAME",
    "INFO_NAME",
    "WARN_NAME",
    "WARNING_NAME",
    "SEVERE_NAME",
    "ERROR_NAME",
    "FATAL_NAME",
    "CRITICAL_NAME",

    "TRACE_ALIAS",
    "DEBUG_ALIAS",
    "INFO_ALIAS",
    "WARN_ALIAS",
    "WARNING_ALIAS",
    "SEVERE_NAME",
    "ERROR_ALIAS",
    "FATAL_ALIAS",
    "CRITICAL_ALIAS",

    "LEVEL",
    "LEVELNAME",
    "DATE",
    "TIME",
    "MOMENT",
    "MICRO",
    "FILE",
    "FILEPATH",
    "FILENAME",
    "PROCESS",
    "THREAD",
    "FUNCTION",
    "LINE",
    "MESSAGE",
    "MARK",

    "FORMAT_SIMPLE",
    "FORMAT_DEFAULT",
    "FORMAT_DEBUG",
    "FORMAT_DEFAULT_EXTEND",
    "FORMAT_DEBUG_EXTEND",

    "LogopBaseException",
    "LoggingIsClosedError",
    "LogLevelAliasNotFoundError",
    "LogLevelExceedsThresholdError",
    "LogFormatInvalidError",
    "TooManyStandardTypeLogopObjectError",
    "ExistingLoggingError",
    "LogopIdentNotFoundError",

    "BaseLogging",
    "Logging",

    "BaseLogop",
    "LogopStandard",
    "LogopStandardPlus",
    "LogopFile",

    "op_character_variable",
    "callabletrack"
]
