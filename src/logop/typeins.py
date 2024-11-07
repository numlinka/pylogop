# Licensed under the MIT License.
# pylogop Copyright (C) 2023 numlinka.

# std
import os
import threading

from types import FrameType
from typing import Tuple, Dict, AnyStr, Callable
from datetime import datetime as DateTime
from threading import Thread
from dataclasses import dataclass, field
from multiprocessing.process import BaseProcess

# internal
from .constants import *


@dataclass
class LevelDetails (object):
    """
    Log level details.

    Contains the log level, name and alias.
    """
    level: int
    alias: str
    name: str


@dataclass
class StateSource (object):
    """
    Information sources for obtaining richer status information.

    Used to obtain information about the current log level, thread, process, etc.
    """
    loglevel: LevelDetails
    datetime: DateTime
    frame: FrameType
    thread: Thread
    process: BaseProcess


@dataclass
class LogDetails (object):
    """
    Log unit details.

    Contains the log unit details.
    """
    # source
    __source: StateSource = field(repr=False)

    # message
    message: str = ""
    mark: str = None

    # level
    level: int = field(init=False)
    level_name: str = field(init=False)
    level_alias: str = field(init=False)

    # datetime
    date: str = field(init=False)
    time: str = field(init=False)
    milli: str = field(init=False)
    micro: str = field(init=False)

    # frame
    module: str = field(init=False)
    filepath: str = field(init=False)
    filename: str = field(init=False)
    function: str = field(init=False)
    line: int = field(init=False)
    file: str = field(init=False)

    # thread
    thread: str = field(init=False)
    thread_name: str = field(init=False)
    thread_ident: int = field(init=False)

    # process
    process: int = field(init=False)

    def __post_init__(self):
        # level
        self.level = self.__source.loglevel.level
        self.level_name = self.__source.loglevel.name
        self.level_alias = self.__source.loglevel.alias

        # datetime
        self.date = self.__source.datetime.strftime("%Y-%m-%d")
        self.time = self.__source.datetime.strftime("%H:%M:%S")
        self.milli = self.__source.datetime.strftime("%f")[:3]
        self.micro = self.__source.datetime.strftime("%f")[3:]

        # frame
        self.module = self.__source.frame.f_globals.get("__name__", "")
        self.filepath = self.__source.frame.f_code.co_filename
        self.filename = os.path.basename(self.filepath)
        self.function = self.__source.frame.f_code.co_name
        self.line = self.__source.frame.f_lineno
        try: self.file = os.path.relpath(self.filepath)
        except Exception as _: self.file = self.filepath

        # thread
        self.thread = self.__source.thread.name
        self.thread_name = self.__source.thread.name
        self.thread_ident = self.__source.thread.ident

        # process
        self.process = self.__source.process.pid

        # others
        if self.mark is None:
            self.mark = self.module

        # ! Frame object cannot be pickle.
        # This will cause asdict to fail, so we need to remove the attribute.
        # But it cannot be really deleted, so you need to assign this property to Ellipsis.
        self.__source = None



@dataclass
class LogUnit (object):
    """
    Log unit.

    In addition to the log unit details, it also contains other formatted content passed by the user.
    """
    details: LogDetails
    args: Tuple[AnyStr]
    kwargs: Dict[str, AnyStr]



class TrackStateUnit (object):
    """
    Track state unit.

    Provided to the `callabletrack` decorator to record the status information it needs to include.
    """
    _lock: threading.RLock
    logging = None

    track_callee = True
    track_result = True
    track_except = True

    callable: Callable = None
    level_alias: str = TRACE_ALIAS

    def __init__(self):
        self._lock = threading.RLock()



__all__ = [
    "LevelDetails",
    "StateSource",
    "LogDetails",
    "LogUnit",
    "TrackStateUnit"
]
