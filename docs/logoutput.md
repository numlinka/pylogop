# pylogop 日志输出对象

LogopStandard、LogopStandardPlus 和 LogopFile，它们都是日志输出对象的不同实现方式。BaseLogop 是基础类，其他类继承自它并实现了具体的日志输出逻辑。

日志输出对象接受来自日志管理器的日志内容和日志格式，并通过自己的方式输出日志。


## logop.logoutput 函数

```Python
.op_character_variable(op_format: str, table: dict) -> str
# 将日志格式转换成完整的日志消息
# op_format: 日志格式
# table: 日志信息表; 通常情况下 BaseLogop.call 可以直接提供 content 参数所接收到的内容 )
```

## logop.logoutput.BaseLogop 日志输出对象

```Python
logop.logoutput.BaseLogop(name: str = ...)
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
# 在日志对象调用输出对象的 call 方法发生异常时会调用这个方法,
# 使得输出对象内部的异常计数 + 1.

.get_logging_onject() -> Union[object, None]
# 获取绑定的日志管理器
# 每个日志输出对象只能绑定一个日志管理器.
# 但未绑定任何日志管理器时返回 None.


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


## LogopStandard 输出对象 标准型

```Python
logop.logoutput.LogopStandard()
# 继承 BaseLogop
# 将日志写到标准输出 stdout / stderr.
```


## LogopStandardPlus 输出对象 标准型 控制台着色

```Python
logop.logoutput.LogopStandardPlus()
# 继承 BaseLogop
# 将日志写到标准输出 stdout / stderr.
```


## LogopFile 日志文件 - 输出对象

```Python
logop.logoutput.Logop_file(name: str = ..., pathdir: Union[str, list, tuple] = 'logs',
                           pathname: str = '$(.date).log', encoding: str = 'utf-8')
# name: 同 BaseLogop
# pathdir: 保存日志文件的文件夹路径, 多级路径可以通过列表和元组的方式传入.
# pathname: 日志的文件名.
# encoding: 文件编码.
```