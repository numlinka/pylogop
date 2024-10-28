# Licensed under the MIT License.
# pylogop Copyright (C) 2023 numlinka.

# std
from typing import AnyStr

# site
from typex import Singleton

# internal
from . import utils
from .logging import Logging
from .constants import *


class _Ease (Singleton):
    @property
    def logging(self) -> Logging:
        return utils.get_default_logging()


ease = _Ease()


def trace(message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
    """
    Log a TRACE message.

    Arguments:
        message (str): The message to be logged; It can be a format spec string.
        *args (AnyStr): The arguments of the format spec string.
        mark (str): The mark of the log message; It will be printed in the log message.
        back_count (int): The number of frames to go back; It is used to get the source information.
        **kwargs (AnyStr): The keyword arguments of the format spec string.
    """
    ease.logging.call(TRACE_ALIAS, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)


def debug(message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
    """
    Log a DEBUG message.

    Arguments:
        message (str): The message to be logged; It can be a format spec string.
        *args (AnyStr): The arguments of the format spec string.
        mark (str): The mark of the log message; It will be printed in the log message.
        back_count (int): The number of frames to go back; It is used to get the source information.
        **kwargs (AnyStr): The keyword arguments of the format spec string.
    """
    ease.logging.call(DEBUG_ALIAS, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)


def info(message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
    """
    Log a INFO message.

    Arguments:
        message (str): The message to be logged; It can be a format spec string.
        *args (AnyStr): The arguments of the format spec string.
        mark (str): The mark of the log message; It will be printed in the log message.
        back_count (int): The number of frames to go back; It is used to get the source information.
        **kwargs (AnyStr): The keyword arguments of the format spec string.
    """
    ease.logging.call(INFO_ALIAS, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)


def warn(message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
    """
    Log a WARN message.

    Arguments:
        message (str): The message to be logged; It can be a format spec string.
        *args (AnyStr): The arguments of the format spec string.
        mark (str): The mark of the log message; It will be printed in the log message.
        back_count (int): The number of frames to go back; It is used to get the source information.
        **kwargs (AnyStr): The keyword arguments of the format spec string.
    """
    ease.logging.call(WARN_ALIAS, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)


def warning(message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
    """
    Log a WARNING message.

    Arguments:
        message (str): The message to be logged; It can be a format spec string.
        *args (AnyStr): The arguments of the format spec string.
        mark (str): The mark of the log message; It will be printed in the log message.
        back_count (int): The number of frames to go back; It is used to get the source information.
        **kwargs (AnyStr): The keyword arguments of the format spec string.
    """
    ease.logging.call(WARNING_ALIAS, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)


def error(message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
    """
    Log a ERROR message.

    Arguments:
        message (str): The message to be logged; It can be a format spec string.
        *args (AnyStr): The arguments of the format spec string.
        mark (str): The mark of the log message; It will be printed in the log message.
        back_count (int): The number of frames to go back; It is used to get the source information.
        **kwargs (AnyStr): The keyword arguments of the format spec string.
    """
    ease.logging.call(ERROR_ALIAS, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)


def severe(message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
    """
    Log a SEVERE message.

    Arguments:
        message (str): The message to be logged; It can be a format spec string.
        *args (AnyStr): The arguments of the format spec string.
        mark (str): The mark of the log message; It will be printed in the log message.
        back_count (int): The number of frames to go back; It is used to get the source information.
        **kwargs (AnyStr): The keyword arguments of the format spec string.
    """
    ease.logging.call(SEVERE_ALIAS, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)


def critical(message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
    """
    Log a CRITICAL message.

    Arguments:
        message (str): The message to be logged; It can be a format spec string.
        *args (AnyStr): The arguments of the format spec string.
        mark (str): The mark of the log message; It will be printed in the log message.
        back_count (int): The number of frames to go back; It is used to get the source information.
        **kwargs (AnyStr): The keyword arguments of the format spec string.
    """
    ease.logging.call(CRITICAL_ALIAS, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)


def fatal(message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
    """
    Log a FATAL message.

    Arguments:
        message (str): The message to be logged; It can be a format spec string.
        *args (AnyStr): The arguments of the format spec string.
        mark (str): The mark of the log message; It will be printed in the log message.
        back_count (int): The number of frames to go back; It is used to get the source information.
        **kwargs (AnyStr): The keyword arguments of the format spec string.
    """
    ease.logging.call(FATAL_ALIAS, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)



__all__ = [
    "ease",
    "trace",
    "debug",
    "info",
    "warn",
    "warning",
    "error",
    "severe",
    "critical",
    "fatal"
]
