# logop

一个简易的日志输出模块



## 安装

使用 pip 安装 logop

`pip install logop`



## 快速上手

```Python
import logop

# 初始化一个日志对象
log = logop.Logging()

# 进行日志输出
log.info('Hello world.')
log.error('Exception.')
```


### 为控制台日志着色

```Python
import logop

# 拒绝日志对象自动初始化一个标准输出对象
log = logop.Logging(stdout=False)

# 初始化一个带控制台着色的标准输出对象
stdob = logop.Logop_standard_up()

# 将输出对象添加到日志对象中
log.add_op(stdob)

# 进行日志输出
log.info('Hello world.')
log.error('Exception.')
```


### 输出日志到文件

```Python
import logop

# 初始化一个日志对象
log = logop.Logging()

# 初始化一个日志文件输出对象
fileob = logop.Logop_file(pathdir='.', pathname='$(.date).log')

log.add_op(fileob)

# 进行日志输出
log.info('Hello world.')
log.error('Exception.')
```


### 自定义日志等级

```Python
import logop

# 初始化一个日志对象
log = logop.Logging()

# 添加日志等级
logop.levelTable['alias1'] = (Logop.INFO, 'name1')
logop.levelTable['alias2'] = (Logop.INFO, 'name2')

# 使用自定义日志等级进行输出
log.alias1('Hello world.')
log.alias2('Hello world.')
```



## 常量

```Python
# 日志等级
logop.ALL
     .TRACE
     .DEBUG
     .INFO
     .WARN
     .WARNING
     .SEVERE
     .ERROR
     .FATAL
     .CRITICAL
     .OFF

# 日志格式
logop.FORMAT.SIMPLE
            .DEFAULT
            .DEBUG
```



## 日志格式可用信息

| 属性名称   | 格式          | 描述         | 数据类型 | 示例          |
| :--------- | :------------ | :----------- | :------- | :------------ |
| .level     | $(.level)     | 日志等级     | int      | 0             |
| .levelname | $(.levelname) | 等级名称     | str      | INFO          |
| .date      | $(.date)      | 日期         | str      | 2020-04-01    |
| .time      | $(.time)      | 时间         | str      | 08:00:00      |
| .moment    | $(.moment)    | 毫秒         | str      | 123           |
| .micro     | $(.micro)     | 微秒         | str      | 512           |
| .file      | $(.file)      | 文件相对路径 | str      | lib/a.py      |
| .filepath  | $(.filepath)  | 文件绝对路径 | str      | /opt/lib/a.py |
| .filename  | $(.filename)  | 文件名       | str      | a.py          |
| .process   | $(.process)   | 进程名       | str      | Process       |
| .thread    | $(.thread)    | 线程名       | str      | Main          |
| .function  | $(.function)  | 函数         | str      | run           |
| .line      | $(.line)      | 行           | int      | 56            |
| .message   | $(.message)   | 消息         | str      | Hello world   |

例: `"[$(.date) $(.time)] [$(.thread)/$(.levelname)] $(.message)"`



## logop 函数

```Python
.op_character_variable(op_format: str, table: dict) -> str
# 将日志格式转换成完整的日志消息
# op_format: 日志格式
# table: 日志信息表; 通常情况下 BaseLogop.call 可以直接提供 content 参数所接收到的内容 )
```



## BaseLogop 输出对象

```Python
logop.BaseLogop(name: str = ...)
# 所有的所有的输出对象都必须继承自 BaseLogop
# name: 设置 op_name 标识, 必须是 str 类型, 否则保持默认.


.call(content: dict, op_format: str = FORMAT.DEFAULT) -> None
# 输出日志
# 在日志对象需要进行输出时会调用这个方法
# content: 日志内容, 通常是日志对象收集到的信息
# op_format: 日志格式
# BaseLogop 的 call 方法不会进行任何输出

.add_exception_count() -> None
# 增加异常计数
# 在日志对象调用输出对象的 call 方法发送异常时会调用这个方法,
# 使得输出对象内部的异常计数 + 1.


.op_type -> str
# 输出对象的类型标识
# 非标准输出对象需要重写这个标识

.op_name -> str
# 输出对象的名称标识
# 可以用于区分同类型的输出对象

.op_ident -> int
# 鉴别标识
# 在输出对象被成功添加到日志对象时会修改这个标识,
# 以保证它在所在日志对象里面是唯一的.

.op_exception_count -> int
# 异常计数
# 记录该输出对象出现异常的次数
```



## Logop_standard (标准)输出对象

```Python
logop.Logop_standard()
# 继承 BaseLogop
# 将日志写到标准输出 stdout / stderr.
```



## Logop_standard_up 简单着色 - (标准)输出对象

```Python
logop.Logop_standard_up()
# 继承 BaseLogop
# 将日志写到标准输出 stdout / stderr.
```



## Logop_file 日志文件 - 输出对象

```Python
logop.Logop_file(name: str = ..., pathdir: Union[str, list, tuple] = 'logs',
                 pathname: str = '$(.date).log', encoding: str = 'utf-8')
# name: 同 BaseLogop
# pathdir: 保存日志文件的文件夹路径, 多级路径可以通过列表和元组的方式传入.
# pathname: 日志的文件名.
# encoding: 文件编码.
```



## Logging 日志对象

```Python
logop.Logging(level: int = INFO, op_format: str = FORMAT.DEFAULT, *, stdout: bool = True,
              asynchronous: bool = False, threadname: str = 'LoggingThread')
# 初始化一个日志对象
# level: 日志等级, 低于这个等级的日志不会被显示/输出, 建议通过日志等级常量设置.
# op_format: 日志格式, 日志消息的组合方式, 输出对象不一定会遵守这个格式.
# stdout: 是否自动初始化一个标准输出对象.
# asynchronous: 创建一个线程让日志对象异步执行.
# threadname: 线程名称, 仅在 asynchronous 为 True 时生效.


.setlevel(level: int) -> None
# 设置日志等级
# 低于这个等级的日志不会被显示/输出, 建议通过日志等级常量设置.

.setformat(op_format: str) -> None
# 设置日志格式
# 日志消息的组合方式, 输出对象不一定会遵守这个格式, 可以通过日志格式常量设置.

.add_op(target: BaseLogop) -> None
# 添加输出对象
# 输出对象的数量不能超过 16 个.
# 输出对象必须继承自 BaseLogop , 且 .op_type 标识为 'standard' 的输出对象只能有一个.
# 该方法会改变输出对象的 op_ident 标识, 以保证它在当前日志对象里面是唯一的.

.del_op(ident: int) -> None
# 删除输出对象
# 将输出对象从日志对象中移除, 提供的 ident 值必须是存在的.
# 当提供一个不存在于日志对象中的 ident 值时会抛出 ValueError 异常.

.get_op_list() -> list[dict]
# 获取输出对象信息列表

.get_op_count() -> int
# 获取输出对象的数量

.get_op_object(ident: int) -> BaseLogop | None
# 获取到输出对象
# 当提供的 ident 标识存在时返回这个输出对象, 否则返回 None.

.get_stdop_object() -> BaseLogop | None
# 获取到标准输出对象
# 当存在标准输出对象时返回输出对象, 否则返回 None.

.call(level: int = INFO, levelname: str = 'INFO', message: str = '',
      *, double_back: bool = False) -> None
# 输出日志
# level: 日志等级, 当等级低于设置等级时不进行日志输出.
# levelname: 日志名称, 任意, 但推荐为 INFO, WARN, ERROR, DEBUG 等标准名称.
# message: 日志消息.
# double_back: 是否要从上上个栈帧中获取状态信息, 对该方法进行包装时会用到它.

.trace(message) -> None
# 输出一个 TRACE 级别的日志

.debug(message) -> None
.info(message) -> None
.warn(message) -> None
.warning(message) -> None
.severe(message) -> None
.error(message) -> None
.fatal(message) -> None
.critical(message) -> None
# 同上
```

