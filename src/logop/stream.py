# Licensed under the MIT License.
# pylogop Copyright (C) 2023 numlinka.

# std
import os
import sys
import threading

from io import TextIOBase
from typing import AnyStr, Union, List
from dataclasses import asdict

# internal
from . import utils
from .base import BaseLogging, BaseOutputStream
from .typeins import LogUnit
from .constants import *
from .exceptions import *


class StandardOutputStream (BaseOutputStream):
    _lock: threading.RLock

    name = STANDARD
    __ident: int = IDENT_EMPTY
    __logging: BaseLogging = None
    __exception_count: int = 0

    def __init__(self, name: str = None):
        """
        Create a new standard output stream.

        It accepts the log message unit passed by the logging object and
        formats it and outputs it to the standard output or error output.

        Arguments:
            name (str): The name of this output stream.
        """
        self._lock = threading.RLock()
        if isinstance(name, str):
            self.name = name

    @property
    def type(self) -> str:
        """The type of this output stream. | **Read only**"""
        return STANDARD

    @property
    def ident(self) -> int:
        """The ident of this output stream. | **Read only**"""
        with self._lock:
            return self.__ident

    @property
    def logging(self) -> BaseLogging:
        """The logging object associated with this output stream | **Read only**"""
        with self._lock:
            return self.__logging

    @property
    def exception_count(self) -> int:
        """The number of exceptions that have been caught by this output stream. | **Read only**"""
        with self._lock:
            return self.__exception_count

    def add_exception_count(self) -> None:
        """
        Add an exception count to this output stream.
        """
        with self._lock:
            self.__exception_count += 1

    def associate(self, logging_object: BaseLogging, ident: int = IDENT_EMPTY) -> None:
        """
        Associate this output stream with a logging object.

        Arguments:
            logging_object (BaseLogging): The logging object to associate with this output stream.
            ident (int): The ident of this output stream.

        Raises:
            TypeError (TypeError): The logging_object is not an instance of AbstractLogging.
            StreamAssociationFailed (StreamAssociationFailed): The output stream is already associated with a logging object.
            StreamVerificationFailed (StreamAssociationFailed): The ident is not valid.
        """
        if not isinstance(logging_object, BaseLogging):
            raise TypeError("The logging_object must be an instance of AbstractLogging.")

        if not isinstance(ident, int):
            raise TypeError("The ident must be an integer.")

        with self._lock:
            if self.logging is not None or self.ident != IDENT_EMPTY:
                raise StreamAssociationFailed("This output stream is already associated with a logging object.")

            if ident == IDENT_EMPTY:
                logging_object.add_stream(self)
                return

            if logging_object.add_stream_verify(self, ident):
                self.__logging = logging_object
                self.__ident = ident
                return

            raise StreamVerificationFailed("The ident is not valid.")

    def disassociate(self, verify: bool = False) -> None:
        """
        Disassociate this output stream with a logging object.

        Arguments:
            verify (bool): You don't need to provide this parameter, Cancel the verification phase of the association.

        Raises:
            StreamVerificationFailed (StreamVerificationFailed): The ident is not valid.
        """
        if not verify:
            self.logging.del_stream(self.ident)
            return

        if self.logging.del_stream_verify(self, self.ident):
            with self._lock:
                self.__logging = None
                self.__ident = IDENT_EMPTY
                return

        raise StreamVerificationFailed("The ident is not valid.")

    def direct(self, value: str, *args: AnyStr, **kwargs: AnyStr) -> None:
        """
        Directly output the content of the message.

        Arguments:
            value (str): The content of the message.
            *args: The arguments of the message.
            **kwargs: The keyword arguments of the message.
        """
        sys.stdout.write(value.format(*args, **kwargs))

    def call(self, log_format: str, log_unit: LogUnit) -> None:
        """
        Output the content of the message.

        Arguments:
            log_format (str): The format of the log message.
            log_unit (LogUnit): The log unit containing the log information.
        """
        content = utils.format_log_message(log_format, log_unit)
        level = log_unit.details.level
        stream = sys.stdout if level < ERROR else sys.stderr
        stream.write(content)
        stream.write(CHAR_LF)
        stream.flush()



class StandardOutputStreamPlus (StandardOutputStream):
    _color_code_map = {
        ALL: "30",
        TRACE: "36",
        DEBUG: "34",
        INFO: "0",
        WARN: "33",
        ERROR: "31",
        CRITICAL: "1;31",
        FATAL: "1;37;41"
    }
    _code_sequences: List[int] = []

    def __init__(self, name: str = None) -> None:
        """
        Create a new standard output stream.

        It accepts the log message unit passed by the logging object and
        formats it and outputs it to the standard output or error output.

        The difference from the normal version is that the Plus version will color the console log.

        Arguments:
            name (str): The name of this output stream.
        """
        super().__init__(name)
        self._lock = threading.RLock()
        utils.set_windows_console_mode()
        self._update_code_sequences()

    def _update_code_sequences(self) -> None:
        with self._lock:
            self._code_sequences = list(self._color_code_map.keys())
            self._code_sequences.sort()

    def _get_color_code(self, level: int = INFO) -> str:
        code = "0"
        with self._lock:
            for strict_level, color_code in self._color_code_map.items():
                if level >= strict_level:
                    code = color_code
                else:
                    break

        return code

    def set_level_color(self, level: int, *colors: str) -> None:
        """
        Set the color of the log level.

        Arguments:
            level (int): The log level.
            *colors (str): The color of the log level.

        Raises:
            LogLevelInvalid (LogLevelInvalid): The level parameter is not a valid log level.
            ValueError (ValueError): The colors parameter must be provided.
            TypeError (TypeError): The color parameter must be a string.
        """
        if not isinstance(level, int) or not ALL <= level <= OFF:
            raise LogLevelInvalid(f"The {level} is not a valid log level.")

        if len(colors) == 0:
            raise ValueError("The colors parameter must be provided.")

        for color in colors:
            if not isinstance(color, str):
                raise TypeError("The color must be a string.")

        with self._lock:
            self._color_code_map[level] = ";".join(colors)
        self._update_code_sequences()


    def call(self, log_format: str, log_unit: LogUnit) -> None:
        content = utils.format_log_message(log_format, log_unit)
        level = log_unit.details.level
        stream = sys.stdout if level < ERROR else sys.stderr
        color_code = self._get_color_code(level)
        stream.write(f"\033[{color_code}m{content}\033[0m{CHAR_LF}")
        stream.flush()



class FileOutputStream (StandardOutputStream):
    __target: Union[str, TextIOBase] = "./logs/{date}.log"

    def __init__(self, name: str = None, target: Union[str, TextIOBase] = None) -> None:
        """
        Create a new file output stream.

        It accepts the log message unit passed by the log object,
        formats it and outputs it to a file or file IO object.

        Arguments:
            name (str): The name of this output stream.
            target (str | TextIOBase): It must be a valid file path or a text IO object.
                If it is a string, it will be formatted with the log unit.
                default: "./logs/{date}.log"
        """
        super().__init__(name)
        self.set_target(target)

    @property
    def type(self) -> str:
        return "file"

    @property
    def target(self) -> Union[str, TextIOBase]:
        with self._lock:
            return self.__target

    def set_target(self, target: Union[str, TextIOBase]) -> None:
        """
        Set the target of this output stream.

        Arguments:
            target (str | TextIOBase): It must be a valid file path or a text IO object.
                If it is a string, it will be formatted with the log unit.
                default: "./logs/{date}.log"

        Raises:
            TypeError (TypeError): The target must be a string or a file object.
        """
        if target is None:
            return

        if not isinstance(target, (str, TextIOBase)):
            raise TypeError("The target must be a string or a file object.")

        with self._lock:
            self.__target = target

    # ! This method is not implemented yet.
    def direct(self, value: str, *args: AnyStr, **kwargs: AnyStr) -> None:
        raise NotImplementedError("This method is not implemented yet.")
        # TODO: Implement this method.
        # This method should not perform any actions until it completes.
        # 2024-10-01 - I haven't figured out how to do this.

    def call(self, log_format: str, log_unit: LogUnit) -> None:
        content = utils.format_log_message(log_format, log_unit)

        if isinstance(self.target, str):
            path = self.target.format(**asdict(log_unit.details))
            dirname = os.path.dirname(path)

            if not os.path.exists(dirname):
                os.makedirs(dirname)

            with open(path, "a", encoding="utf-8") as file:
                file.write(content)
                file.write(CHAR_LF)
                file.flush()

        elif isinstance(self.target, TextIOBase):
            self.target.write(content)
            self.target.write(CHAR_LF)
            self.target.flush()

        else:
            raise TypeError("The target must be a string or a file object.")



__all__ = [
    "StandardOutputStream",
    "StandardOutputStreamPlus",
    "FileOutputStream"
]
