# Licensed under the MIT License.
# pylogop Copyright (C) 2023 numlinka.

class LogopBaseException (Exception):
    """Logop base exception."""

class LogLevelInvalid (LogopBaseException):
    """The log level is invalid."""

class LogLevelNotExists (LogopBaseException):
    """The log level does not exist."""

class LogLevelAliasInvalid (LogopBaseException):
    """The log level alias is invalid."""

class LogLevelAliasExists (LogopBaseException):
    """The log level alias already exists."""

class LogLevelAliasNotExists (LogopBaseException):
    """The log level alias does not exist."""

class StreamVerificationFailed (LogopBaseException):
    """The stream verification failed."""

class LoggingIsClosed (LogopBaseException):
    """The logging object is closed."""

class OutputStreamNotExist (LogopBaseException):
    """The output stream does not exist."""


__all__ = [x for x in dir() if not x.startswith("_")]
