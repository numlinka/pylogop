# Licensed under the MIT License.
# logop by numlinka.

# std
from typing import *

# local
from .formats import *
from .logging_base import *


class BaseLogop (object):
    """Log output object."""
    op_name = "standard"  # Object name, used to distinguish objects of the same type.
    op_type = "standard"  # An object type that distinguishes its implementation
    op_ident = 0  # It's unique in the logger where it's located.
    op_logging_object: BaseLogging = None
    op_exception_count = 0

    def __init__(self, name: str = ..., **_):
        self.op_name = name if isinstance(name, str) else "standard"

    def call(self, content: dict, op_format: str = FORMAT_DEFAULT) -> None:
        if not isinstance(content, dict):
            raise TypeError("The content type is not dict.")

        if not isinstance(op_format, str):
            raise TypeError("The op_format type is not str.")

        if "$(.message)" not in op_format:
            raise ValueError("$(.message) must be included in format.")

    def add_exception_count(self) -> None:
        self.op_exception_count += 1

    def get_logging_onject(self) -> Union[object, None]:
        return self.op_logging_object


__all__ = ["BaseLogop"]
