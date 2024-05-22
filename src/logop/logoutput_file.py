# Licensed under the MIT License.
# logop by numlinka.

# std
import os
from typing import *

# self
from .logoutput_base import *

# local
from .utils import *
from .formats import *


class LogopFile (BaseLogop):
    """Log file Indicates the log output object.

    Output log information to a log file.
    """
    op_name = "logfile"
    op_type = "logfile"

    def __init__(self, name: str = "logfile", directory: Union[str, Iterable] = "logs",
                 filename: str = "$(.date).log", encoding: str = "utf-8"):
        super().__init__(name)

        if not isinstance(directory, (str, Iterable)):
            raise TypeError("The pathdir type is not str or Iterable.")

        if not isinstance(filename, str):
            raise TypeError("The pathname type is not str.")

        if isinstance(directory, str):
            self._directory = directory

        elif isinstance(directory, Iterable):
            self._directory = os.path.join(*directory)

        else:
            raise Exception("Errors that should not occur.")

        self._filename = filename
        self._encoding = encoding

    def call(self, content: dict, op_format: str = FORMAT_DEFAULT) -> None:
        super().call(content, op_format)

        targetdir = op_character_variable(self._directory, content)
        targetname = op_character_variable(self._filename, content)
        targetfile = os.path.join(targetdir, targetname)

        op = op_character_variable(op_format, content)
        ops = f"{op}\n"
        if not os.path.isdir(targetdir):
            os.makedirs(targetdir)

        with open(targetfile, "a", encoding=self._encoding) as fob:
            fob.write(ops)
            fob.flush()


__all__ = ["LogopFile"]
