# pylogop

pylogop 是一个轻量型的日志模块，用于记录日志信息。


## 特点

* 多样化的日志输出格式：pylogop 提供了不同的日志输出格式，可以根据需求选择适合的格式，例如标准输出格式、文件输出格式等。

* 灵活的日志级别设置：可以根据需要设置不同的日志级别，从而控制日志消息的详细程度。常见的日志级别包括DEBUG、INFO、WARNING、ERROR和CRITICAL。

* 多种日志输出方式：pylogop 支持将日志消息输出到标准输出、文件等多种目标。这样可以根据实际需求选择合适的输出方式，方便日志的收集和查看。

* 异步日志记录：pylogop 支持异步日志记录，可以在后台线程中处理日志消息。这种方式可以提高性能，尤其是在高并发或频繁日志记录的情况下。

* 简单易用的接口：pylogop 的接口设计简单明了，使用起来非常方便。通过调用相应的方法或设置相应的参数，就可以完成日志记录的配置和操作。

* 可扩展性：pylogop 的代码结构清晰，采用面向对象的设计，易于扩展和定制。可以根据需要添加新的日志输出方式或定制日志记录逻辑。


## 安装

推荐使用 pip 按安装 pylogop

`pip install logop`

或更新 pylogop 以使用新版本的特性

`pip install --upgrade logop`


## 快速上手

导入 pylogop 模块

```Python
import logop
```

希望将日志消息输出到控制台

```Python
# 初始化一个日志管理对象
logging = logop.logging.Logging()
```

或希望将带有颜色的日志消息输出到控制台

```Python
# 拒绝日志管理对象自动初始化一个标准型日志输出对象
logging = logop.logging.Logging(stdout=False)

# 初始化一个带有颜色的标准型日志输出对象
logoutput = logop.logoutput.LogopStandardPlus()

# 将日志输出对象添加到日志管理对象
logging.add_op(logoutput)
```

或希望将日志消息输出到文件

```Python
# 初始化一个日志管理对象
logging = logop.logging.Logging()

# 初始化一个文件型日志输出对象
logoutput = logop.logoutput.LogopFile()

# 将日志输出对象添加到日志管理对象
logging.add_op(logoutput)
```

输出日志

```Python
logging.info("Hello word")
logging.warn("WARN")
logging.error("ERROR")
logging.fatal("FATAL ERROR")
```


## 设计

Logging 类是日志管理器，它可以添加和删除日志输出对象，并根据日志级别过滤日志消息。它还支持异步日志记录，可以在后台线程中处理日志消息，以提高性能。

BaseLogop、LogopStandard、LogopStandardPlus 和 LogopFile，它们都是日志输出对象的不同实现方式。BaseLogop 是基础类，其他类继承自它并实现了具体的日志输出逻辑。


## 改动

1.0.0 版本模块的结构发生了改动，但仍可以通过以下方式直接使用旧版本的代码

```Python
import logop.old as logop
```


## 文档

- [日志等级](docs/level.md)

- [日志格式](docs/format.md)

- [日志管理器](docs/logging.md)

- [日志输出对象](docs/logoutput.md)
