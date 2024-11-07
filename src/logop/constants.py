# Licensed under the MIT License.
# pylogop Copyright (C) 2023 numlinka.

"""
constants
"""

# level
"""
     ┌────────────────────────────────────  ALL
~ 0x7F E D C B A 9 8 7 6 5 4 3 2 1 0  ━┳━━  Undefined / Special Purpose
~ 0x6F E D C B A 9 8 7 6 5 4 3 2 1 0  ━┫
~ 0x5F E D C B A 9 8 7 6 5 4 3 2 1 0  ━┫
~ 0x4F E D C B A 9 8 7 6 5 4 3 2 1 0  ━┛
~ 0x3F E D C B A 9 8 7 6 5 4 3 2 1 0  ━┳━━  TRACE
~ 0x2F E D C B A 9 8 7 6 5 4 3 2 1 0  ━┛
~ 0x1F E D C B A 9 8 7 6 5 4 3 2 1 0  ━┳━━  DEBUG
~ 0x0F E D C B A 9 8 7 6 5 4 3 2 1 0  ━┛
  0x00 1 2 3 4 5 6 7 8 9 A B C D E F  ━┳━━  INFO
  0x10 1 2 3 4 5 6 7 8 9 A B C D E F  ━┛
  0x20 1 2 3 4 5 6 7 8 9 A B C D E F  ━┳━━  WARN / WARNING
  0x30 1 2 3 4 5 6 7 8 9 A B C D E F  ━┛
  0x40 1 2 3 4 5 6 7 8 9 A B C D E F  ━┳━━  ERROR
  0x50 1 2 3 4 5 6 7 8 9 A B C D E F  ━┛
  0x60 1 2 3 4 5 6 7 8 9 A B C D E F  ━━━━  SEVERE / CRITICAL
  0x70 1 2 3 4 5 6 7 8 9 A B C D E F  ━━━━  FATAL
                                   └──────  OFF
"""
ALL = ~ 0x7F
TRACE = - 0x40
DEBUG = - 0x20
INFO = 0x00
WARN = 0x20
WARNING = 0x20
ERROR = 0x40
SEVERE = 0x60
CRITICAL = 0x60
FATAL = 0x70
OFF = 0x7F

TRACE_NAME = "TRACE"
DEBUG_NAME = "DEBUG"
INFO_NAME = "INFO"
WARN_NAME = "WARN"
WARNING_NAME = "WARNING"
ERROR_NAME = "ERROR"
SEVERE_NAME = "SEVERE"
CRITICAL_NAME = "CRITICAL"
FATAL_NAME = "FATAL"

TRACE_ALIAS = "trace"
DEBUG_ALIAS = "debug"
INFO_ALIAS = "info"
WARN_ALIAS = "warn"
WARNING_ALIAS = "warning"
ERROR_ALIAS = "error"
SEVERE_ALIAS = "severe"
CRITICAL_ALIAS = "critical"
FATAL_ALIAS = "fatal"

# keywords
MESSAGE = "message"
MARK = "mark"

LEVEL = "level"
LEVEL_NAME = "level_name"
LEVEL_ALIAS = "level_alias"

DATE = "date"
TIME = "time"
MILLI = "milli"
MICRO = "micro"

MODULE = "module"
FILEPATH = "filepath"
FILENAME = "filename"
FUNCTION = "function"
FILE = "file"
LINE = "line"

THREAD = "thread"
PROCESS_NAME = "process_name"
PROCESS_IDENT = "thread_ident"

PROCESS = "process"

# stream type
STANDARD = "standard"

# ident
IDENT_EMPTY = -1

# name
DEFAULT_THREAD_NAME = "LoggingThread"
IDENT_COUNTER = "logop_ident_counter"
LOG_ID_COUNTER = "logop_log_id_counter"

# others
CHAR_LF = "\n"


CALLABLE_TRACK_CALLEE_FORMAT = """calltrack lid-{lid:08} call
\tcaller: File "{caller_filename}", line {caller_lineno} in {caller_name}
\tcallee: File "{callee_filename}", line {callee_lineno} in {callee_name}
\targs: {track_args}\n\tkwargs: {track_kwargs}"""

CALLABLE_TRACK_RESULT_FORMAT = """calltrack lid-{lid:08} return
\t{result_type} {result_value}"""

CALLABLE_TRACK_EXCEPT_FORMAT = """calltrack lid-{lid:08} except
{traceback_msg}"""


class FORMAT:
    DEFAULT = "[{date} {time}] [{thread}/{level_name}] {message}"
    SIMPLE = "[{level_name}] {message}"
    VERY_SIMPLE = "[{level_name:.1}] {message}"
    DEBUG = "[{date} {time}.{milli}] [{thread}/{level_name}] {message} ({mark})"
    TRACE = "[{date} {time}.{milli}{micro}] {file}: {line} [{thread}/{level_name}] {message} ({mark})"



__all__ = [x for x in dir() if x[0] != "_"]
