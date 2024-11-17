# Licensed under the MIT License.
# pylogop Copyright (C) 2023 numlinka.

# std
import sys
import copy

from typing import Union, Callable, Tuple, Dict, Any, AnyStr
from dataclasses import asdict

# internal
from . import _state
from .base import BaseLogging
from .logging import Logging
from .typeins import LevelDetails, LogUnit
from .constants import *
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

    Raises:
        LogLevelAliasNotExists (LogLevelAliasNotExists): If the level parameter is not a valid log level alias.
        LogLevelNotExists (LogLevelNotExists): If the level parameter is not a valid log level.
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


def secure_format(format_spec: str, *format_args: Tuple[AnyStr], **format_kwargs: Dict[str, AnyStr]) -> str:
    """
    Safely formats a string using the specified format arguments and keyword arguments.

    It handles IndexError and KeyError exceptions and tries to add placeholders to the format arguments and keyword arguments.

    Arguments:
        format_spec (str): The format string to be formatted.
        *format_args (Tuple[AnyStr]): The tuple of arguments to be used in the format string.
        **format_kwargs (Dict[str, AnyStr]): The dictionary of keyword arguments to be used in the format string.

    Returns:
        result (str): The formatted string.
    """
    count = 0
    format_args = list(format_args)

    while True:
        try:
            if count > SECURE_FORMAT_MAXIMUM_NUMBER_OF_CORRECTIONS: raise ValueError
            result = format_spec.format(*format_args, **format_kwargs)

        except IndexError as _:
            format_args.append("{}")
            count += 1
            continue

        except KeyError as e:
            key = str(e)[1:-1]
            format_kwargs[key] = f"{{{key}}}"
            count += 1
            continue

        except Exception as _:
            for key, value in format_kwargs.items():
                format_spec = format_spec.replace(f"{{{key}}}", value)

            else:
                return format_spec

        else:
            return result


def format_log_message_secure(log_format: str, log_unit: LogUnit) -> str:
    """
    Formats a log message using the specified format string and log unit.

    However, compared to the standard format function, it guarantees that there will be output, but with some loss of detail.

    Recommended only if the standard formatting process reports an error.

    Arguments:
        log_format (str): The format string for the log message.
        log_unit (LogUnit): The log unit containing the log information.

    Returns:
        message (str): The formatted log message.
    """
    try:
        format_kwargs = asdict(log_unit.details)
        content = secure_format(log_format, **format_kwargs)
        format_kwargs.update(log_unit.kwargs)
        return secure_format(content, *log_unit.args, **format_kwargs)

    except Exception as _:
        return log_format


def format_log_message(log_format: str, log_unit: LogUnit) -> str:
    """
    Formats a log message using the specified format string and log unit.

    Arguments:
        log_format (str): The format string for the log message.
        log_unit (LogUnit): The log unit containing the log information.

    Returns:
        message (str): The formatted log message.
    """
    try:
        format_kwargs = asdict(log_unit.details)
        content = log_format.format(**format_kwargs)
        format_kwargs.update(log_unit.kwargs)
        return content.format(*log_unit.args, **format_kwargs)

    except Exception as _:
        return format_log_message_secure(log_format, log_unit)


def add_log_level(level: int, alias: str, name: str) -> None:
    """
    Adds a new log level.

    Arguments:
        level (int): Log level, used to determine the importance of the log and whether it will be filtered.
        alias (str): Alias of the log level, usually a lowercase string, used for indexing, must be unique.
        name (str): The name of the log level, usually an uppercase string, for display purposes.

    Raises:
        LogLevelInvalid (LogLevelInvalid): If the level parameter is not a valid log level.
        LogLevelAliasExists (LogLevelAliasExists): If the alias parameter is already in use.
    """
    if not isinstance(level, int) or not ALL <= level <= OFF:
        raise LogLevelInvalid(f"The {level} is not a valid log level.")

    with _state.lock:
        if alias in _state.level_map:
            raise LogLevelAliasExists(f"The alias '{alias}' is already in use.")

        _state.level_map[alias] = LevelDetails(level, alias, name)


def del_log_level(alias: str) -> None:
    """
    Deletes a log level.

    Arguments:
        alias (str): Alias of the log level to delete.

    Raises:
        LogLevelAliasNotExists (LogLevelAliasNotExists): If the alias parameter is not a valid log level alias.
    """
    with _state.lock:
        if alias not in _state.level_map:
            raise LogLevelAliasNotExists(f"The alias '{alias}' does not exist.")

        del _state.level_map[alias]


def set_default_logging(logging_object: BaseLogging, force: bool = False) -> None:
    """
    Set the default logging object.

    Arguments:
        logging_object (BaseLogging): The logging object to set as default.
        force (bool): Whether to force the setting of the default logging object.

    Raises:
        TypeError (TypeError): If the logging_object parameter is not an instance of BaseLogging.
    """
    if not isinstance(logging_object, BaseLogging):
        raise TypeError("The logging object must be an instance of BaseLogging.")

    with _state.lock:
        if not isinstance(_state._default_logging, BaseLogging) or force:
            _state._default_logging = logging_object
            return


def get_default_logging() -> Logging:
    """
    Returns the default logging object.

    If the default logging object is not set, it will be created and returned.

    Returns:
        logging (Logging): The default logging object.
    """
    with _state.lock:
        if not isinstance(_state._default_logging, BaseLogging):
            new_logging = Logging()
            set_default_logging(new_logging)

        return _state._default_logging


__all__ = [
    "try_execute",
    "level_details",
    "set_windows_console_mode",
    "format_log_message",
    "add_log_level",
    "del_log_level"
]
