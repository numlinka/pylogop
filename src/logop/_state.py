# Licensed under the MIT License.
# pylogop Copyright (C) 2023 numlinka.

# std
from threading import RLock

# internal
from .base import BaseLogging
from .typeins import LevelDetails, Atomic
from .constants import *

atomic: Atomic = Atomic()
lock = RLock()

_default_logging: BaseLogging = ...

level_map = {
    TRACE_ALIAS: LevelDetails(TRACE, TRACE_ALIAS, TRACE_NAME),
    DEBUG_ALIAS: LevelDetails(DEBUG, DEBUG_ALIAS, DEBUG_NAME),
    INFO_ALIAS: LevelDetails(INFO, INFO_ALIAS, INFO_NAME),
    WARN_ALIAS: LevelDetails(WARN, WARN_ALIAS, WARN_NAME),
    WARNING_ALIAS: LevelDetails(WARNING, WARNING_ALIAS, WARNING_NAME),
    ERROR_ALIAS: LevelDetails(ERROR, ERROR_ALIAS, ERROR_NAME),
    SEVERE_ALIAS: LevelDetails(SEVERE, SEVERE_ALIAS, SEVERE_NAME),
    CRITICAL_ALIAS: LevelDetails(CRITICAL, CRITICAL_ALIAS, CRITICAL_NAME),
    FATAL_ALIAS: LevelDetails(FATAL, FATAL_ALIAS, FATAL_NAME)
}


__all__ = []
