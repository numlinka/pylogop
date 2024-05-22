# Licensed under the MIT License.
# logop by numlinka.

# std
import threading
from typing import *

# self
from .logging_base import *


class Atomic (object):
    def __init__(self):
        self.value: int
        self.__lock = threading.RLock()
        self.__count = 0

    def __getattr__(self, __name: str) -> Any:
        if __name != "value":
            return super().__getattr__(__name)

        with self.__lock:
            value = self.__count
            self.__count += 1
            return value


class TrackStateUnit (object):
    _lock = threading.RLock()
    logging: BaseLogging = ...

    track_callee = True
    track_result = True
    track_except = False


__all__ = [
    "Atomic",
    "TrackStateUnit"
]
