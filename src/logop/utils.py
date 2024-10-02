# Licensed under the MIT License.
# pylogop Copyright (C) 2023 numlinka.

# std
import sys
import copy

from typing import Union, Callable, Any
from dataclasses import asdict

# internal
from . import _state
from .typeins import LevelDetails, LogUnit
from .exceptions import *


def try_execute(func: Callable, fallback_value: Any = None, *args: Any, **kwargs: Any) -> Any:
    """
    Executes a function and returns a fallback value if an exception occurs.

    Arguments:
        func (Callable): The function to execute.
        fallback_value (Any): The value to return if an exception occurs.
        *args (Any): Additional arguments to pass to the function.
        **kwargs (Any): Additional keyword arguments to pass to the function.

    Returns:
        Any (Any): The result of the function execution or the fallback value if an exception occurs.
    """
    try:
        return func(*args, **kwargs)

    except Exception as _:
        return fallback_value


def level_details(level: Union[str, int]) -> LevelDetails:
    """
    Returns the details of a log level.

    Arguments:
        level (str | int): The log level or its alias.

    Returns:
        LevelDetails (LevelDetails): The details of the specified log level.
    """
    with _state.lock:
        if isinstance(level, str):
            if level not in _state.level_map:
                raise LogLevelAliasNotExists(level)

            return copy.copy(_state.level_map[level])

        elif isinstance(level, int):
            for _, details in _state.level_map.items():
                if details.level == level:
                    return copy.copy(details)

            else:
                raise LogLevelNotExists(level)

        else:
            raise TypeError("The level parameter must be an integer or a string.")


def set_windows_console_mode() -> bool:
    """
    Sets the Windows console mode to enable ANSI escape codes.

    Returns:
        success (bool): `True` if the operation was successful, `False` otherwise.
    """
    if sys.platform != "win32":
        return False

    try:
        from ctypes import windll
        kernel32 = windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        return True

    except ImportError:
        return False


def format_log_message(log_format: str, log_unit: LogUnit) -> str:
    """
    Formats a log message using the specified format string and log unit.

    Arguments:
        log_format (str): The format string for the log message.
        log_unit (LogUnit): The log unit containing the log information.

    Returns:
        message (str): The formatted log message.
    """
    format_spec = asdict(log_unit.details)
    content = log_format.format(**format_spec)
    format_spec.update(log_unit.kwargs)
    return content.format(**format_spec)


__all__ = [
    "try_execute",
    "level_details",
]
