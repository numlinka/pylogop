# -*- codeing:utf-8 -*-

# *project:     pylogop
# *Author:      numLinka


import os
import sys
import inspect
import datetime
import threading
import multiprocessing

from typing import Union


__version__ = "0.4.0"


ALL      = - 0x80
TRACE    = - 0x40   # - 0x50 -> - 0x31
DEBUG    = - 0x20   # - 0x30 -> - 0x11
INFO     =   0x00   # - 0x10 ->   0x0F   stdout
WARN     =   0x20   #   0x10 ->   0x2F   stderr
WARNING  =   0x20
SEVERE   =   0x30
ERROR    =   0x40   #   0x30 ->   0x4F
FATAL    =   0x60   #   0x50 ->   0x6F
CRITICAL =   0x60
OFF      =   0x7F



VARIABLE_TABLE = """ $(variable)
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
"""



class FORMAT(object):
    # 朴素
    SIMPLE = '[$(.levelname)] $(.message)'

    # 默认
    DEFAULT = '[$(.date) $(.time)] [$(.thread)/$(.levelname)] $(.message)'

    # 调试
    DEBUG = '[$(.date) $(.time).$(.moment)] $(.file) [$(.thread)/$(.levelname)] [line:$(.line)] $(.message)'



levelTable = {
    'trace': (TRACE, 'TRACE'),
    'debug': (DEBUG, 'DEBUG'),
    'info': (INFO, 'INFO'),
    'warn': (WARN, 'WARN'),
    'warning': (WARNING, 'WARNING'),
    'severe': (SEVERE, 'SEVERE'),
    'error': (ERROR, 'ERROR'),
    'fatal': (FATAL, 'FATAL'),
    'critical': (CRITICAL, 'CRITICAL')
}



def op_character_variable(op_format: str, table: dict) -> str:
    if not isinstance(op_format, str):
        raise TypeError('op_format is not of type str')

    if not isinstance(table, dict):
        raise TypeError('table is not of type dict')

    op = op_format
    for key, value in table.items():
        op = op.replace(f'$(.{key})', f'{value}')

    return op



class BaseLogop(object):
    op_type = 'standard'
    op_name = 'standard'
    op_ident = 0
    op_exception_count = 0

    def __init__(self, name: str = ...):
        if isinstance(name, str):
            self.op_name = name


    def call(self, content: dict, op_format: str = FORMAT.DEFAULT) -> None:
        ...


    def add_exception_count(self) -> None:
        self.op_exception_count += 1



class Logop_standard(BaseLogop):
    def call(self, content: dict, op_format: str = FORMAT.DEFAULT) -> None:
        if not isinstance(content, dict):
            raise TypeError('content is not of type dict')

        if not isinstance(op_format, str):
            raise TypeError('op_format is not of type str')

        if '$(.message)' not in op_format:
            raise ValueError('$(.message) must be included in format')

        op = op_character_variable(op_format, content)
        ops = f'{op}\n'
        level = content.get('level', 0)

        if level < 0x10:
            sys.stdout.write(ops)
            sys.stdout.flush()

        else:
            sys.stderr.write(ops)
            sys.stdout.flush()



class Logop_standard_up(BaseLogop):
    def call(self, content: dict, op_format: str = FORMAT.DEFAULT) -> None:
        if not isinstance(content, dict):
            raise TypeError('content is not of type dict')

        if not isinstance(op_format, str):
            raise TypeError('op_format is not of type str')

        if '$(.message)' not in op_format:
            raise ValueError('$(.message) must be included in format')

        op = op_character_variable(op_format, content)
        level = content.get('level', 0)
        if level < 0x10:
            ops = f'{op}\n'

        elif 0x10 <= level < 0x40:
            ops = f'\033[1;33m{op}\033[0m\n'

        elif 0x40 <= level < 0x80:
            ops = f'\033[1;31m{op}\033[0m\n'

        else:
            ops = f'{op}\n'

        if level < 0x10:
            sys.stdout.write(ops)
            sys.stdout.flush()

        else:
            sys.stderr.write(ops)
            sys.stdout.flush()



class Logop_file(BaseLogop):
    op_name = 'logfile'
    op_type = 'logfile'


    def __init__(self, name: str = ..., pathdir: Union[str, list, tuple] = 'logs',
                 pathname: str = '$(.date).log', encoding: str = 'utf-8'):
        if isinstance(name, str):
            self.op_name = name

        if not isinstance(pathdir, (str, list, tuple)):
            raise TypeError('The pathdir type is not str, list or tuple')

        if not isinstance(pathname, str):
            raise TypeError('The pathname type is not str')

        if isinstance(pathdir, str):
            self._pathdir = pathdir

        elif isinstance(pathdir, (list, tuple)):
            self._pathdir = os.path.join(pathdir)

        else:
            raise Exception('Errors that should not occur')

        self._pathname = pathname
        self._encoding = encoding


    #! fallibility
    def call(self, content: dict, op_format: str = FORMAT.DEFAULT) -> None:
        targetdir = op_character_variable(self._pathdir, content)
        targetname = op_character_variable(self._pathname, content)
        targetfile = os.path.join(targetdir, targetname)

        op = op_character_variable(op_format, content)
        ops = f'{op}\n'
        if not os.path.isdir(targetdir):
            os.makedirs(targetdir)

        with open(targetfile, 'a', encoding=self._encoding) as fob:
            fob.write(ops)
            fob.flush()



class Logging(object):
    __level = INFO
    __op_format = FORMAT.DEFAULT
    __op_list = []


    def __init__(self, level: int = INFO, op_format: str = FORMAT.DEFAULT,
                 *, stdout: bool = True, asynchronous: bool = False, threadname: str = 'LoggingThread'):
        self.__call_lock = threading.RLock()
        self.__set_lock = threading.RLock()

        self.setlevel(level)
        self.setformat(op_format)

        if stdout: self.add_op(Logop_standard())

        self.__asynchronous = True if asynchronous else False

        if self.__asynchronous:
            self.__call_event = threading.Event()
            self.__message_list = []
            self.__asynchronous_task = threading.Thread(None,self.__run_cycle, threadname, (), {}, daemon=True)
            self.__asynchronous_task.start()


    def setlevel(self, level: int) -> None:
        with self.__set_lock:
            if not isinstance(level, int):
                raise TypeError('level is not of type int')

            if not -0x80 <= level <= 0x7F:
                raise ValueError('level should be somewhere between -0x80 to 0x7F ')

            self.__level = level


    def setformat(self, op_format: str) -> None:
        with self.__set_lock:
            if not isinstance(op_format, str):
                raise TypeError('op_format is not of type str')

            if '$(.message)' not in op_format:
                raise ValueError('$(.message) must be included in format')

            self.__op_format = op_format

    #! fallibility
    def add_op(self, target: BaseLogop) -> None:
        with self.__set_lock:
            if not isinstance(target, BaseLogop):
                raise TypeError('The target type is not op_object')

            if len(self.__op_list) > 0x10:
                raise Warning('There are too many op objects')

            standard = BaseLogop.op_type
            typelist = [x.op_type for x in self.__op_list]

            if standard in typelist and target.op_type == standard:
                raise ValueError('Only one standard op_object can exist')

            identlist = [x.op_ident for x in self.__op_list]
            if identlist:
                ident = max(identlist) + 1
            else:
                ident = 1

            target.op_ident = ident

            self.__op_list.append(target)

    #! fallibility
    def del_op(self, ident: int) -> None:
        with self.__set_lock:
            for index, op in enumerate(self.__op_list):
                if op.op_ident == ident:
                    break
            else:
                raise ValueError('The ident value does not exist')

            del self.__op_list[index]

    #! fallibility
    def get_op_list(self) -> list:
        with self.__set_lock:
            answer = []
            for item in self.__op_list:
                answer.append({
                    'op_ident': item.op_ident,
                    'op_name': item.op_name,
                    'op_type': item.op_type,
                    'exception_count': item.op_exception_count
                })
            return answer


    def get_op_count(self) -> int:
        with self.__set_lock:
            count = len(self.__op_list)
            return count

    #! fallibility
    def get_op_object(self, ident: int) -> Union[BaseLogop, None]:
        with self.__set_lock:
            for opobj in self.__op_list:
                if opobj.op_ident == ident:
                    return opobj

            else:
                return None

    #! fallibility
    def get_stdop_object(self) -> Union[BaseLogop, None]:
        with self.__set_lock:
            for opobj in self.__op_list:
                if opobj.op_type == BaseLogop.op_type:
                    return opobj

            else:
                return None

    #! fallibility
    def get_stdop_ident(self) -> Union[int, None]:
        with self.__set_lock:
            for opobj in self.__op_list:
                if opobj.op_type == BaseLogop.op_type:
                    return opobj.op_ident

            else:
                return None

    #! fallibility
    def __try_op_call(self, content: dict) -> None:
        with self.__set_lock:
            call_list = self.__op_list.copy()

        with self.__call_lock:
            for stdop in call_list:
                try: stdop.call(content, self.__op_format)
                except Exception:
                    try: stdop.add_exception_count()
                    except Exception: ...


    def __try_op_call_asynchronous(self) -> None:
        with self.__call_lock:
            if not len(self.__message_list): return None

            content = self.__message_list[0]
            del self.__message_list[0]

        self.__try_op_call(content)

        with self.__call_lock:
            if not len(self.__message_list): return None
            else: self.__try_op_call_asynchronous()


    def __run_cycle(self, *args, **kwds):
        while True:
            self.__call_event.wait()
            self.__try_op_call_asynchronous()
            self.__call_event.clear()


    def __run_call_asynchronous(self, content: dict) -> None:
        with self.__call_lock: self.__message_list.append(content)
        self.__call_event.set()


    def __run_call(self, content: dict) -> None:
        if self.__asynchronous: self.__run_call_asynchronous(content)
        else: self.__try_op_call(content)


    def call(self, level: int = INFO, levelname: str = 'INFO', message: str = '', *, double_back: bool = False) -> None:
        if level < self.__level: return None

        now = datetime.datetime.now()

        content = {}
        content['level'] = level
        content['levelname'] = levelname
        content['message'] = message

        content['date'] = now.strftime('%Y-%m-%d')
        content['time'] = now.strftime('%H:%M:%S')
        content['moment'] = now.strftime('%f')[:3]
        content['micro'] = now.strftime('%f')[3:]

        content['process'] = multiprocessing.current_process().name
        content['thread'] = threading.current_thread().name

        if double_back: frame = inspect.currentframe().f_back.f_back
        else: frame = inspect.currentframe().f_back

        abspath = os.path.abspath(frame.f_code.co_filename)
        local = os.path.join(sys.path[0], '')
        slen = len(local)
        if abspath[:slen] == local: file = abspath[slen:]
        else: file = abspath

        content['file'] = file
        content['filepath'] = abspath
        content['filename'] = os.path.basename(file)
        content['function'] = frame.f_code.co_name
        content['line'] = frame.f_lineno

        self.__run_call(content)


    def __get_call(self, alias: str = 'info'):
        def call_table(message: object = ''):
            nonlocal self
            nonlocal alias
            level, name = levelTable[alias]
            self.call(level, name, message, double_back=True)

        return call_table


    def trace(self, message: object = ''):
        self.call(TRACE, 'TRACE', message, double_back=True)

    def debug(self, message: object = ''):
        self.call(DEBUG, 'DEBUG', message, double_back=True)

    def info(self, message: object = ''):
        self.call(INFO, 'INFO', message, double_back=True)

    def warn(self, message: object = ''):
        self.call(WARN, 'WARN', message, double_back=True)

    def warning(self, message: object = ''):
        self.call(WARNING, 'WARNING', message, double_back=True)

    def severe(self, message: object = ''):
        self.call(SEVERE, 'SEVERE', message, double_back=True)

    def error(self, message: object = ''):
        self.call(ERROR, 'ERROR', message, double_back=True)

    def fatal(self, message: object = ''):
        self.call(FATAL, 'FATAL', message, double_back=True)

    def critical(self, message: object = ''):
        self.call(CRITICAL, 'CRITICAL', message, double_back=True)


    def __getattr__(self, __name):
        if __name in levelTable: return self.__get_call(__name)
        else: raise AttributeError('This alias is not defined in the level table')
