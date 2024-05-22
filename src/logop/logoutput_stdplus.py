# Licensed under the MIT License.
# logop by numlinka.

# std
import sys

# self
from .logoutput_base import *

# local
from .utils import *
from .levels import *
from .formats import *


class LogopStandardPlus (BaseLogop):
    """Standard log output object. Plus.

    Outputs the colored log information to the console.
    """

    def __init__(self, name: str = ..., **_):
        super().__init__(name)
        self.__color_code = {
            INFO: "30",
            WARN: "0",
            ERROR: "1;33",
            OFF: "1;31",
        }
        set_windows_console_mode()

    def _get_color_code(self, level) -> str:
        for astrict_level, color_code in self.__color_code.items():
            if level < astrict_level:
                return color_code

        else:
            return "0"

    def call(self, content: dict, op_format: str = FORMAT_DEFAULT) -> None:
        super().call(content, op_format)

        op = op_character_variable(op_format, content)
        level = content.get("level", 0)

        color_code = self._get_color_code(level)

        ops = f"\033[{color_code}m{op}\033[0m\n"

        if level < ERROR:
            sys.stdout.write(ops)
            sys.stdout.flush()

        else:
            sys.stderr.write(ops)
            sys.stderr.flush()


__all__ = ["LogopStandardPlus"]
