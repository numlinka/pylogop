# Licensed under the MIT License.
# logop by numlinka.

# std
from abc import *
from typing import *


class BaseLogging (ABC):
    @abstractmethod
    def call(self, *args, **kwargs) -> None: ...


__all__ = ["BaseLogging"]
