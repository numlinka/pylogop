# Licensed under the MIT License.
# pylogop Copyright (C) 2023 numlinka.

# std
import sys
import inspect
import datetime
import threading
import multiprocessing
from typing import Union, Optional, List, Dict, AnyStr, Callable

# internal
from . import _state
from . import utils
from .base import BaseLogging, BaseOutputStream
from .stream import StandardOutputStream
from .typeins import StateSource, LogDetails, LogUnit
from .constants import *
from .exceptions import *


class Logging (BaseLogging):
    __level: int
    __format: str

    def __init__(self, log_level: Union[str, int] = INFO, log_format: str = FORMAT.DEFAULT, *,
                 stdout: bool = True, asynchronous: bool = False, thread_name: str = DEFAULT_THREAD_NAME,
                 daemon: bool = True) -> None:
        """
        If you don't allow it to automatically initialize a standard output stream,
        then you need to add the output stream yourself, otherwise it won't output anything.

        In synchronous mode, the time consumed by calling the output stream is borne by the calling thread,
        if you don't want this, please use asynchronous mode.

        Arguments:
            log_level (str | int): log level; It must be a valid log level or alias; default: INFO.
            log_format (str): log format; It must be a format string; default: FORMAT.DEFAULT.
            stdout (bool): Whether to output to the standard output stream; default: True.
            asynchronous (bool): Whether to use asynchronous output; default: False.
            thread_name (str): The name of the thread used for asynchronous output; default: DEFAULT_THREAD_NAME.
            daemon (bool): Whether the thread used for asynchronous output is a daemon thread; default: True.
        """
        self._lock_set = threading.RLock()
        self._lock_call = threading.RLock()
        self._lock_message = threading.RLock()
        self._lock_stream = threading.RLock()

        self._list_message: List[LogUnit] = []
        self._list_stream: List[BaseOutputStream] = []
        self._unverified_stream_add: Dict[int, BaseOutputStream] = {}
        self._unverified_stream_del: Dict[int, BaseOutputStream] = {}

        self.__is_paused = False
        self.__is_closed = False
        self.__is_async = False

        self.__level: int
        self.__format: str
        self.__temp_stdout: Optional[StandardOutputStream] = ...

        self.set_level(log_level)
        self.set_format(log_format)

        if stdout:
            self.add_stream(StandardOutputStream())

        if asynchronous:
            self.__is_async = True
            self.__async_event = threading.Event()
            self.__async_thread = threading.Thread(target=self.__async_mainloop, name=thread_name, daemon=daemon)
            self.__async_thread.start()

        utils.set_default_logging(self)

    @property
    def level(self) -> int:
        """The current log level. | **Read only**"""
        with self._lock_set:
            return self.__level

    @property
    def log_format(self) -> str:
        """The current log format. | **Read only**"""
        with self._lock_set:
            return self.__format

    @property
    def is_paused(self) -> bool:
        """Status of paused. | **Read only**"""
        with self._lock_set:
            return self.__is_paused

    @property
    def is_closed(self) -> bool:
        """Status of closed. | **Read only**"""
        with self._lock_set:
            return self.__is_closed

    @property
    def is_async(self) -> bool:
        """Status of asynchronous mode. | **Read only**"""
        with self._lock_set:
            return self.__is_async

    @property
    def stdout(self) -> StandardOutputStream:
        """
        Standard output stream. | **Read only**

        Get the standard output stream in the output stream list.
        If there is no standard output stream, a temporary one is automatically created.

        This temporary standard output stream will not be added to the list.
        """
        with self._lock_stream:
            for stream in self._list_stream:
                if stream.type == STANDARD:
                    return stream

            if isinstance(self.__temp_stdout, StandardOutputStream):
                return self.__temp_stdout

            self.__temp_stdout = StandardOutputStream()
            return self.__temp_stdout

    def exist_stdout_stream(self) -> bool:
        """
        Check whether the standard output stream exists in the output stream list.
        """
        with self._lock_stream:
            for stream in self._list_stream:
                if stream.type == STANDARD:
                    return True

            return False

    def set_level(self, level: Union[str, int]) -> None:
        """
        Set log level.

        Logs below this level are filtered.

        Arguments:
            level (str | int): log level; It must be a valid log level or alias.

        Raises:
            TypeError (TypeError): If the level type is not str or int.
            LogLevelInvalid (LogLevelInvalid): If the level is not a valid log level or alias.
        """
        if isinstance(level, str):
            ld = utils.level_details(level)
            new_level = ld.level

        elif isinstance(level, int):
            if ALL <= level <= OFF:
                new_level = level
            else:
                raise LogLevelInvalid(f"The {level} is not a valid log level or alias.")

        else:
            raise TypeError("The level must be a string or an integer.")

        with self._lock_set:
            self.__level = new_level

    def set_format(self, log_format: str) -> None:
        """
        Set log format.

        The format of the output log content,
        `Logging` does not process the log content, but passes it to the `OutputStream` object.

        Arguments:
            log_format (str): log format; It must be a format string.

        Raises:
            TypeError (TypeError): If the log_format type is not str.
        """
        if not isinstance(log_format, str):
            raise TypeError("The log_format type is not str.")

        with self._lock_set:
            self.__format = log_format

    def pause(self) -> None:
        """
        Pause logging.

        While paused, new log messages will be temporarily stored in a list until unpause.
        """
        with self._lock_set:
            self.__is_paused = True

    def unpause(self) -> None:
        """
        Unpause logging.

        At the same time, the logs temporarily stored in the list will be output immediately.
        """
        with self._lock_set:
            self.__is_paused = False
        self.__spark()

    def close(self) -> None:
        """
        Close logging.

        After closing, no new log messages will be accepted,
        and the system will wait for unprinted log messages to be output.

        Raises:
            LoggingIsClosed (LoggingIsClosed): If the logging object is closed.
        """
        self.__close_check()

        with self._lock_set:
            self.__is_closed = True

        if self.is_async:
            self.__async_event.set()

    def clear_message(self) -> None:
        """
        Clear the log message list.
        """
        with self._lock_message:
            self._list_message.clear()

    def clear(self) -> None:
        """
        Clear the log message list.
        """
        self.clear_message()

    def add_stream(self, stream: BaseOutputStream) -> int:
        """
        Add an output stream.

        It should be noted that only one standard output stream object can be added.

        Arguments:
            stream (BaseOutputStream): output stream.

        Returns:
            ident (int): The identifier of the added stream.

        Raises:
            StreamVerificationFailed (StreamVerificationFailed): If the stream is not verified.
        """
        with self._lock_stream:
            if stream.type == STANDARD and self.exist_stdout_stream():
                raise StreamVerificationFailed("Only one standard output stream object can be added.")

            ident = _state.atomic_ident.value
            self._unverified_stream_add[ident] = stream

        stream.associate(self, ident)
        return ident

    def add_stream_verify(self, stream: BaseOutputStream, ident: int) -> bool:
        """
        Verify the addition of an output stream.

        This method is called by the `add_stream` method.

        Arguments:
            stream (BaseOutputStream): output stream.
            ident (int): The identifier of the stream.

        Returns:
            success (bool): Whether the verification is successful.
        """
        with self._lock_stream:
            if ident not in self._unverified_stream_add:
                return False

            if self._unverified_stream_add[ident] is not stream:
                return False

            self._list_stream.append(stream)
            del self._unverified_stream_add[ident]
            return True

    def del_stream(self, ident: int) -> None:
        """
        Remove an output stream.

        Arguments:
            ident (int): The identifier of the stream.

        Raises:
            OutputStreamNotExist (OutputStreamNotExist): If the ident does not exist.
        """
        with self._lock_stream:
            for stream in self._list_stream:
                if stream.ident == ident:
                    self._unverified_stream_del[ident] = stream
                    stream.disassociate(True)
                    break

            else:
                raise OutputStreamNotExist(f"The ident {ident} does not exist")

    def del_stream_verify(self, stream: BaseOutputStream, ident: int) -> bool:
        """
        Verify the removal of an output stream.

        This method is called by the `del_stream` method.

        Arguments:
            stream (BaseOutputStream): output stream.
            ident (int): The identifier of the stream.

        Returns:
            success (bool): Whether the verification is successful.
        """
        with self._lock_stream:
            if ident not in self._unverified_stream_del:
                return False

            if self._unverified_stream_del[ident] is not stream:
                return False

            self._list_stream.remove(stream)
            del self._unverified_stream_del[ident]
            return True

    def get_stream(self, ident: int) -> BaseOutputStream:
        """
        Get the output stream.

        Arguments:
            ident (int): The identifier of the stream.

        Returns:
            stream (BaseOutputStream): output stream.

        Raises:
            OutputStreamNotExist: If the ident does not exist.
        """
        with self._lock_stream:
            for stream in self._list_stream:
                if stream.ident == ident:
                    return stream

            else:
                raise OutputStreamNotExist(f"The ident {ident} does not exist")

    def get_stream_list(self) -> List[BaseOutputStream]:
        """
        Get the list of output streams.

        Returns:
            stream_list (List[BaseOutputStream]): The list of output streams.
        """
        with self._lock_stream:
            return self._list_stream.copy()

    def __close_check(self) -> None:
        """
        Check whether the logging object is closed.

        The main purpose is to prevent certain methods from being called after closing.
        In fact, only a few internal methods use it.
        In most cases it is convenient to access `is_closed` directly.

        Raises:
            LoggingIsClosed (LoggingIsClosed): If the logging object is closed.
        """
        if self.is_closed:
            raise LoggingIsClosed("The logging object is closed.")

    def __try_call_stream(self) -> None:
        """
        Call the output stream.

        Pop the message units in the message list one by one, and then call the output stream one by one.

        In synchronous mode, these performance costs are borne by the calling thread.
        """
        while True:
            with self._lock_message:
                if not self._list_message:
                    return 

                unit = self._list_message.pop(0)

            if unit.details.level < self.level:
                continue

            with self._lock_stream:
                for stream in self._list_stream:
                    if utils.try_execute(stream.call, 1, self.log_format, unit) != 1:
                        continue

                    utils.try_execute(stream.add_exception_count, None)

    def __async_mainloop(self, *_) -> None:
        """
        The main loop of the asynchronous mode.

        It is a threading task.
        It will wait for the event to be set, and then call the output stream.
        """
        while True:
            self.__async_event.wait()
            self.__async_event.clear()

            if self.is_paused:
                continue

            if self.is_closed:
                sys.exit()

            self.__try_call_stream()

    def __spark(self):
        """
        Trigger the output stream.
        """
        if self.__is_async:
            self.__async_event.set()
        else:
            self.__try_call_stream()

    def call(self, log_level: Union[int, str], log_message: str, *args: AnyStr,
             log_mark: AnyStr = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
        """
        New log message.

        Arguments:
            log_level (int | str): The level of the log message; It must be a valid log level or alias.
            log_message (str): The message to be logged; It can be a format spec string.
            *args (AnyStr): The arguments of the format spec string.
            log_mark (AnyStr): The mark of the log message; It will be printed in the log message.
            back_count (int): The number of frames to go back; It is used to get the source information.
            **kwargs (AnyStr): The keyword arguments of the format spec string.
        """
        self.__close_check()

        if not isinstance(back_count, int) or back_count < 0:
            back_count = 0

        with self._lock_call:
            now = datetime.datetime.now()
            level_details = utils.level_details(log_level)
            frame = inspect.currentframe()

            for _ in range(back_count + 1):
                frame = frame.f_back

            source = StateSource(
                level_details, now, frame,
                threading.current_thread(),
                multiprocessing.current_process()
            )

            details = LogDetails(source, log_message, log_mark)
            unit = LogUnit(details, args, kwargs)

        with self._lock_message:
            self._list_message.append(unit)

        if self.is_paused:
            return

        self.__spark()

    def trace(self, message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
        """
        Log a TRACE message.

        Arguments:
            message (str): The message to be logged; It can be a format spec string.
            *args (AnyStr): The arguments of the format spec string.
            mark (str): The mark of the log message; It will be printed in the log message.
            back_count (int): The number of frames to go back; It is used to get the source information.
            **kwargs (AnyStr): The keyword arguments of the format spec string.
        """
        self.call(TRACE_ALIAS, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)

    def debug(self, message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
        """
        Log a DEBUG message.

        Arguments:
            message (str): The message to be logged; It can be a format spec string.
            *args (AnyStr): The arguments of the format spec string.
            mark (str): The mark of the log message; It will be printed in the log message.
            back_count (int): The number of frames to go back; It is used to get the source information.
            **kwargs (AnyStr): The keyword arguments of the format spec string.
        """
        self.call(DEBUG_ALIAS, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)

    def info(self, message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
        """
        Log a INFO message.

        Arguments:
            message (str): The message to be logged; It can be a format spec string.
            *args (AnyStr): The arguments of the format spec string.
            mark (str): The mark of the log message; It will be printed in the log message.
            back_count (int): The number of frames to go back; It is used to get the source information.
            **kwargs (AnyStr): The keyword arguments of the format spec string.
        """
        self.call(INFO_ALIAS, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)

    def warn(self, message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
        """
        Log a WARN message.

        Arguments:
            message (str): The message to be logged; It can be a format spec string.
            *args (AnyStr): The arguments of the format spec string.
            mark (str): The mark of the log message; It will be printed in the log message.
            back_count (int): The number of frames to go back; It is used to get the source information.
            **kwargs (AnyStr): The keyword arguments of the format spec string.
        """
        self.call(WARN_ALIAS, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)

    def warning(self, message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
        """
        Log a WARNING message.

        Arguments:
            message (str): The message to be logged; It can be a format spec string.
            *args (AnyStr): The arguments of the format spec string.
            mark (str): The mark of the log message; It will be printed in the log message.
            back_count (int): The number of frames to go back; It is used to get the source information.
            **kwargs (AnyStr): The keyword arguments of the format spec string.
        """
        self.call(WARNING_ALIAS, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)

    def error(self, message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
        """
        Log a ERROR message.

        Arguments:
            message (str): The message to be logged; It can be a format spec string.
            *args (AnyStr): The arguments of the format spec string.
            mark (str): The mark of the log message; It will be printed in the log message.
            back_count (int): The number of frames to go back; It is used to get the source information.
            **kwargs (AnyStr): The keyword arguments of the format spec string.
        """
        self.call(ERROR_ALIAS, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)

    def severe(self, message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
        """
        Log a SEVERE message.

        Arguments:
            message (str): The message to be logged; It can be a format spec string.
            *args (AnyStr): The arguments of the format spec string.
            mark (str): The mark of the log message; It will be printed in the log message.
            back_count (int): The number of frames to go back; It is used to get the source information.
            **kwargs (AnyStr): The keyword arguments of the format spec string.
        """
        self.call(SEVERE_ALIAS, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)

    def critical(self, message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
        """
        Log a CRITICAL message.

        Arguments:
            message (str): The message to be logged; It can be a format spec string.
            *args (AnyStr): The arguments of the format spec string.
            mark (str): The mark of the log message; It will be printed in the log message.
            back_count (int): The number of frames to go back; It is used to get the source information.
            **kwargs (AnyStr): The keyword arguments of the format spec string.
        """
        self.call(CRITICAL_ALIAS, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)

    def fatal(self, message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
        """
        Log a FATAL message.

        Arguments:
            message (str): The message to be logged; It can be a format spec string.
            *args (AnyStr): The arguments of the format spec string.
            mark (str): The mark of the log message; It will be printed in the log message.
            back_count (int): The number of frames to go back; It is used to get the source information.
            **kwargs (AnyStr): The keyword arguments of the format spec string.
        """
        self.call(FATAL_ALIAS, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)

    def get_custom_call(self, alias: str) -> Callable[[str], None]:
        """
        Get a custom log call function.

        Arguments:
            alias (str): The alias of the custom log level.

        Returns:
            callable (Callable): The custom log call function.
        """
        def call_(message: str = "", *args: AnyStr, mark: str = ..., back_count: int = 0, **kwargs: AnyStr) -> None:
            nonlocal alias
            self.call(alias, message, *args, log_mark=mark, back_count=back_count+1, **kwargs)

        return call_

    def __getattr__(self, name: str) -> Callable[[str], None]:
        return self.get_custom_call(name)



__all__ = ["Logging"]
