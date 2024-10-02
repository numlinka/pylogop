# Licensed under the MIT License.
# pylogop Copyright (C) 2023 numlinka.

# std
from abc import ABC, abstractmethod
from typing import *

# internal
from .typeins import LogUnit
from .constants import *


class BaseLogging: ...
class BaseOutputStream: ...


class BaseLogging (ABC):
    """
    The logging object.

    Its main job is to be called by users, collect log and status information,
    package them into log units and hand them over to the output stream object.
    """
    level: int
    log_format: str
    is_paused: bool
    is_closed: bool
    is_async: bool
    stdout: BaseOutputStream

    @abstractmethod
    def set_level(self, level: Union[str, int]) -> None: ...

    @abstractmethod
    def set_format(self, format_: str) -> None: ...

    @abstractmethod
    def pause(self) -> None: ...

    @abstractmethod
    def unpause(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def add_stream(self, stream: BaseOutputStream) -> int: ...

    @abstractmethod
    def add_stream_verify(self, stream: BaseOutputStream, ident: int) -> bool: ...

    @abstractmethod
    def del_stream(self, ident: int) -> None: ...

    @abstractmethod
    def del_stream_verify(self, stream: BaseOutputStream, ident: int) -> bool: ...

    @abstractmethod
    def call(self, log_level: Union[int, str], log_message: str, *args: AnyStr, log_mark: AnyStr = ..., back_count: int = 0, **kwargs: AnyStr) -> None: ...

    @abstractmethod
    def debug(self, message: str = "", *args, mark: str = ..., back_count: int = 0, **kwargs) -> None: ...

    @abstractmethod
    def info(self, message: str = "", *args, mark: str = ..., back_count: int = 0, **kwargs) -> None: ...

    @abstractmethod
    def warn(self, message: str = "", *args, mark: str = ..., back_count: int = 0, **kwargs) -> None: ...

    @abstractmethod
    def error(self, message: str = "", *args, mark: str = ..., back_count: int = 0, **kwargs) -> None: ...

    @abstractmethod
    def fatal(self, message: str = "", *args, mark: str = ..., back_count: int = 0, **kwargs) -> None: ...



class BaseOutputStream (ABC):
    """
    The output stream object.

    Its main job is to output log messages to the specified location in a suitable format and manner.
    """
    name: str
    type: str
    ident: int
    logging: BaseLogging
    exception_count: int

    @abstractmethod
    def add_exception_count(self) -> None: ...

    @abstractmethod
    def associate(self, logging_object: BaseLogging, ident: int = IDENT_EMPTY) -> None: ...

    @abstractmethod
    def disassociate(self, verify: bool = False) -> None: ...

    @abstractmethod
    def direct(self, value: str, *format_spec: AnyStr, **kwargs: AnyStr) -> None: ...

    @abstractmethod
    def call(self, log_format: str, log_unit: LogUnit) -> None: ...



__all__ = ["BaseLogging", "BaseOutputStream"]
