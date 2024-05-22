# Licensed under the MIT License.
# logop by numlinka.

# std
import sys
import inspect
import traceback

from types import *
from typing import *

# self
from .units import *
from .levels import *
from .logging_base import *


_atomic = Atomic()


def callabletrack(
        function: Callable = ..., *, callee: bool = ..., result: bool = ...,
        exception: bool = ..., logging: BaseLogging = ..., level: str | int = ...
        ):
    s_function = function
    s_state = TrackStateUnit()
    if isinstance(callee, bool):
        s_state.track_callee = callee

    if isinstance(result, bool):
        s_state.track_result = result

    if isinstance(exception, bool):
        s_state.track_except = exception

    if isinstance(logging, BaseLogging):
        s_state.logging = logging

    s_level_alias = TRACE_ALIAS

    def level_correct(reference: str | int = ...):
        nonlocal s_level_alias

        if reference is Ellipsis:
            s_level_alias = TRACE_ALIAS

        elif isinstance(reference, (str, int)):
            for lv_alias, (lv, lv_name) in LEVEL_TABLE.items():
                if reference in [lv_alias, lv, lv_name]:
                    s_level_alias = lv_alias
                    break

            else:
                s_level_alias = TRACE_ALIAS

        else:
            s_level_alias = TRACE_ALIAS

    def log(level_alias: str = ..., message: str = "", mark: str = "", *, back_count: int = 0):
        nonlocal s_state, s_level_alias

        if level_alias is Ellipsis:
            level_alias = s_level_alias

        level, levelname = LEVEL_TABLE[level_alias]

        if isinstance(s_state.logging, BaseLogging):
            s_state.logging.call(level, levelname, message, mark, back_count=back_count + 1)
            return

        return

    def log_callee(iid: int, caller_frame: FrameType, args: Iterable, kwargs: Mapping, *, back_count: int = 0):
        nonlocal s_state, s_function

        msg = f"calltrack iid-{iid}\n"
        msg += f"\tcaller: File \"{caller_frame.f_code.co_filename}\", line {caller_frame.f_lineno} in {caller_frame.f_code.co_name}\n"
        msg += f"\tcallee: File \"{s_function.__code__.co_filename}\", line {s_function.__code__.co_firstlineno} in {s_function.__name__}\n"
        msg += f"\targs: {args}\n\tkwargs: {kwargs}\n\twait return"
        log(..., msg, back_count=back_count + 1)

    def log_result(iid: int, result: Any, *, back_count: int = 0):
        nonlocal s_state

        msg = f"calltrack iid-{iid} return: {result}"
        log(..., msg, back_count=back_count + 1)

    def shell(*args, **kwargs):
        nonlocal s_state, s_function

        iid = _atomic.value

        if s_state.track_callee:
            currentframe = inspect.currentframe()
            caller_frame = currentframe.f_back
            log_callee(iid, caller_frame, args, kwargs, back_count=1)

        if s_state.track_except:
            try:
                result = s_function(*args, **kwargs)

            except Exception as e:
                # TODO: Improve exception tracking in callabletrack.
                # When there is an error in the parameter transmission, the exception information does not come from
                # the original function, but from within callabletrack. I don't know any way to improve this.
                # But it'sreally not the information I want.
                exc = traceback.format_exc()
                log(ERROR_ALIAS, exc, back_count=1)
                raise e

        else:
            result = s_function(*args, **kwargs)

        if s_state.track_result:
            log_result(iid, result, back_count=1)

        return result

    def decorate(function: Callable):
        nonlocal s_function

        s_function = function
        return shell

    level_correct(level)

    if callable(function):
        return shell

    else:
        return decorate


__all__ = ["callabletrack"]
