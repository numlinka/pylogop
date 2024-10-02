# Licensed under the MIT License.
# pylogop Copyright (C) 2023 numlinka.

# internal
from . import _state
from .logging import Logging


class _Ease (object):
    @property
    def logging(self) -> Logging:
        with _state.lock:
            if not isinstance(_state._default_logging, Logging):
                _state._default_logging = Logging()

        return _state._default_logging


ease = _Ease()


__all__ = []
