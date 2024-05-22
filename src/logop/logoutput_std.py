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


class LogopStandard (BaseLogop):
    """Standard log output object.

    Output log information to the console.
    """

    def call(self, content: dict, op_format: str = FORMAT_DEFAULT) -> None:
        super().call(content, op_format)

        op = op_character_variable(op_format, content)
        ops = f"{op}\n"
        level = content.get("level", 0)

        if level < ERROR:
            sys.stdout.write(ops)
            sys.stdout.flush()

        else:
            sys.stderr.write(ops)
            sys.stderr.flush()


__all__ = ["LogopStandard"]
