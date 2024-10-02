# Licensed under the MIT License.
# logop by numlinka.

# std
import inspect
import traceback

from types import FrameType
from typing import Callable, Union, Iterable, Mapping, Any, Optional

# self
from . import _ease
from . import _state
from . import utils
from .base import BaseLogging
from .typeins import TrackStateUnit
from .constants import *


def callabletrack(
        function: Callable = ..., *, callee: bool = ..., result: bool = ...,
        exception: bool = ..., logging: Optional[BaseLogging] = ..., level: Union[str, int] = ...
        ):
    """
    Decorator for tracking function calls.

    Arguments:
        function (Callable): The function to be decorated.
        callee (bool): Whether to track the caller and callee of the function.
        result (bool): Whether to track the return value of the function.
        exception (bool): Whether to track exceptions raised by the function.
        logging (BaseLogging): The logging instance to use for tracking.
        level (str | int): The level to use for tracking.
    """
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

    def level_correct(reference: Union[str, int] = ...):
        nonlocal s_level_alias

        if reference is Ellipsis:
            s_level_alias = TRACE_ALIAS
            return

        s_level_alias = utils.level_details(reference).alias

    def log(level_alias: str = ..., message: str = "", mark: str = "", *, back_count: int = 0, **kwargs):
        nonlocal s_state, s_level_alias

        if level_alias is Ellipsis:
            level_alias = s_level_alias

        logging = s_state.logging if s_state.logging is not Ellipsis else _ease.ease.logging
        logging.call(level_alias, message, log_mark=mark, back_count=back_count + 1, **kwargs)

    def log_callee(iid: int, caller_frame: FrameType, args: Iterable, kwargs: Mapping, *, back_count: int = 0):
        nonlocal s_state, s_function

        msg = f"calltrack iid-{iid:04}\n"
        msg += f"\tcaller: File \"{caller_frame.f_code.co_filename}\", line {caller_frame.f_lineno} in {caller_frame.f_code.co_name}\n"
        msg += f"\tcallee: File \"{s_function.__code__.co_filename}\", line {s_function.__code__.co_firstlineno} in {s_function.__name__}\n"
        msg += "\targs: {track_args}\n\tkwargs: {track_kwargs}\n\twait return"
        log(..., msg, back_count=back_count + 1, track_args=args, track_kwargs=kwargs)

    def log_result(iid: int, result: Any, *, back_count: int = 0):
        nonlocal s_state

        msg = f"calltrack iid-{iid:04} return: {result}"
        log(..., msg, back_count=back_count + 1)

    def shell(*args, **kwargs):
        nonlocal s_state, s_function

        iid = _state.atomic.value

        if s_state.track_callee:
            currentframe = inspect.currentframe()
            caller_frame = currentframe.f_back
            log_callee(iid, caller_frame, args, kwargs, back_count=1)

        if s_state.track_except:
            try:
                result = s_function(*args, **kwargs)

            except BaseException as e:
                # TODO: Improve exception tracking in callabletrack.
                # When there is an error in the parameter transmission, the exception information does not come from
                # the original function, but from within callabletrack. I don't know any way to improve this.
                # But it'sreally not the information I want.
                exc = traceback.format_exc()
                log(ERROR_ALIAS, f"calltrack iid-{iid:04}\n{exc}", back_count=1)
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
