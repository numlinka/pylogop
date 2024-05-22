# Licensed under the MIT License.
# logop by numlinka.


LEVEL = "level"
LEVELNAME = "levelname"
DATE = "date"
TIME = "time"
MOMENT = "moment"
MICRO = "micro"
FILE = "file"
FILEPATH = "filepath"
FILENAME = "filename"
PROCESS = "process"
THREAD = "thread"
FUNCTION = "function"
LINE = "line"
MESSAGE = "message"
MARK = "mark"

FORMAT_SIMPLE = "[$(.levelname)] $(.message)"
FORMAT_DEFAULT = "[$(.date) $(.time)] [$(.thread)/$(.levelname)] $(.message)"
FORMAT_DEBUG = "[$(.date) $(.time).$(.moment)] $(.file) [$(.thread)/$(.levelname)] [line:$(.line)] $(.message)"

FORMAT_DEFAULT_EXTEND = "[$(.date) $(.time)] [$(.thread)/$(.levelname)] $(.message) ($(.mark))"
FORMAT_DEBUG_EXTEND = "[$(.date) $(.time).$(.moment)] $(.file) [$(.thread)/$(.levelname)] [line:$(.line)] $(.message) ($(.mark))"

_VARIABLE_TABLE = """ $(variable)
.level      日志等级
.levelname  等级名称
.date       日期
.time       时间
.moment     毫秒
.micro      微秒
.file       文件相对路径
.filepath   文件绝对路径
.filename   文件名
.process    进程名
.thread     线程名
.function   函数
.line       行
.message    消息
.mark       标记名称
"""

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"


__all__ = [
    "LEVEL",
    "LEVELNAME",
    "DATE",
    "TIME",
    "MOMENT",
    "MICRO",
    "FILE",
    "FILEPATH",
    "FILENAME",
    "PROCESS",
    "THREAD",
    "FUNCTION",
    "LINE",
    "MESSAGE",
    "MARK",

    "FORMAT_SIMPLE",
    "FORMAT_DEFAULT",
    "FORMAT_DEBUG",
    "FORMAT_DEFAULT_EXTEND",
    "FORMAT_DEBUG_EXTEND",

    "DATE_FORMAT",
    "TIME_FORMAT"
]
