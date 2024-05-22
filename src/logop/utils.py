# Licensed under the MIT License.
# logop by numlinka.

# std
import sys
from typing import *


def op_character_variable(op_format: AnyStr, table: dict) -> str:
    if not isinstance(op_format, str):
        raise TypeError("The op_format type is not str.")

    if not isinstance(table, dict):
        raise TypeError("The table type is not dict.")

    op = op_format
    for key, value in table.items():
        op = op.replace(f"$(.{key})", f"{value}")

    return op


def set_windows_console_mode() -> bool:
    if sys.platform == "win32":
        try:
            from ctypes import windll
            kernel32 = windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True

        except ImportError:
            return False

    return False


__all__ = [
    "op_character_variable",
    "set_windows_console_mode"
]
