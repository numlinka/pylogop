# Licensed under the MIT License.
# logop by numlinka.

# std
import inspect
import traceback

from types import FrameType
from typing import Callable, Union, Iterable, Mapping, Any, Optional, AnyStr

# self
from . import _ease
from . import _state
from . import utils
from .base import BaseLogging
from .typeins import TrackStateUnit
from .constants import *


def callabletrack(
        callable_: Callable = None, *, callee: bool = None, result: bool = None,
        exception: bool = None, logging: Optional[BaseLogging] = None, level: Union[str, int] = None
        ) -> Callable:
    """
    Decorator for tracking function calls.

    Arguments:
        callable (Callable): The function to be decorated.
        callee (bool): Whether to track the caller and callee of the function.
        result (bool): Whether to track the return value of the function.
        exception (bool): Whether to track exceptions raised by the function.
        logging (BaseLogging): The logging instance to use for tracking.
        level (str | int): The level to use for tracking.

    Returns:
        decorater (Callable): The decorated function or the decorator waiting for the decorated function.
    """
    self = TrackStateUnit()

    if callable(callable_):
        self.callable = callable_

    if callee is not None:
        self.track_callee = bool(callee)

    if result is not None:
        self.track_result = bool(result)

    if exception is not None:
        self.track_except = bool(exception)

    if isinstance(logging, BaseLogging):
        self.logging = logging

    if level is not None:
        self.level_alias = utils.level_details(level).alias

    def log(level_alias: str = None, message: str = "", *args: AnyStr, mark: AnyStr = None, back_count: int = 0, **kwargs: AnyStr) -> None:
        nonlocal self

        if level_alias is None:
            level_alias = self.level_alias

        logging = self.logging if self.logging is not None else _ease.ease.logging
        logging.call(level_alias, message, *args, log_mark=mark, back_count=back_count + 1, **kwargs)

    def shell(*args, **kwargs) -> None:
        nonlocal self

        lid = _state.atomic_lid.value

        if self.track_callee:
            currentframe = inspect.currentframe()
            caller_frame = currentframe.f_back
            log(None, CALLABLE_TRACK_CALLEE_FORMAT,
                lid=lid,
                caller_filename=caller_frame.f_code.co_filename,
                caller_lineno=caller_frame.f_lineno,
                caller_name=caller_frame.f_code.co_name,
                callee_filename=self.callable.__code__.co_filename,
                callee_lineno=self.callable.__code__.co_firstlineno,
                callee_name=self.callable.__name__,
                track_args=args, track_kwargs=kwargs,
                back_count=1)

        if self.track_except:
            try:
                result = self.callable(*args, **kwargs)

            except BaseException as e:
                # TODO: Improve exception tracking in callabletrack.
                # When there is an error in the parameter transmission, the exception information does not come from
                # the original function, but from within callabletrack. I don't know any way to improve this.
                # But it'sreally not the information I want.
                exc = traceback.format_exc()
                log(ERROR_ALIAS, CALLABLE_TRACK_EXCEPT_FORMAT, lid=lid, traceback_msg=exc, back_count=1)
                raise e

        else:
            result = self.callable(*args, **kwargs)

        if self.track_result:
            log(None, CALLABLE_TRACK_RESULT_FORMAT, lid=lid, result_type=type(result), result_value=result, back_count=1)

        return result

    def decorate(callable_: Callable) -> Callable:
        nonlocal self

        self.callable = callable_
        return shell

    if callable_ is None:
        return decorate

    return shell


__all__ = ["callabletrack"]
