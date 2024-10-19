# Licensed under the MIT License.
# pylogop Copyright (C) 2023 numlinka.

# site
from typex import Singleton

# internal
from . import utils
from .logging import Logging


class _Ease (Singleton):
    @property
    def logging(self) -> Logging:
        return utils.get_default_logging()


ease = _Ease()


__all__ = []
