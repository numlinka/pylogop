<div align="center">
  <a style="text-decoration:none" href="https://github.com/numlinka/pylogop">
    <img width="128px" src="favicon.png" alt="pylogop">
  </a>
</dev>

<div align="center">

  # pylogop

  _This is a lightweight and scalable Python logging library._

</div>


<div align="center">
  <a style="text-decoration:none" href="https://opensource.org/license/mit">
    <img src="https://img.shields.io/badge/License-MIT-lightblue" alt="MIT"/>
  </a>
  <a style="text-decoration:none" href="https://pypi.org/project/logop">
    <img src="https://img.shields.io/badge/releases-v1.2.2-lightblue" alt="releases"/>
  </a>
  <a style="text-decoration:none" href="https://pypi.org/project/logop">
    <img src="https://img.shields.io/badge/PyPI-logop-lightblue" alt="PyPI"/>
  </a>
  <a style="text-decoration:none" href="https://www.python.org">
    <img src="https://img.shields.io/badge/Python-3.7+-lightblue" alt="Python3.7+"/>
  </a>
</div>

<p></p>

<!-- <div align="center">

  [English](docs/README_en.md)　|　[简体中文](docs/README_zh.md)

</div> -->


<div align="left" style="max-width: 1000px;">


## Introduce 介绍

This is a lightweight and scalable Python logging library.
It is a library independent from [simplepylibs](https://github.com/numlinka/simplepylibs).<br/>
这是一个轻量级且可扩展的 Python 日志库。
它是从 [simplepylibs](https://github.com/numlinka/simplepylibs) 中独立出来的一部分。


## Install 安装

The preferred way to install logop is via pip.<br/>
推荐使用 pip 安装 logop 。

```bash
pip install logop
```

To upgrade logop to the latest version, use the following command:<br/>
要将 logop 升级到最新版本，请使用以下命令：

```shell
pip install --upgrade logop
```


## Usage 使用

### Basic usage 基础用法

Here is a simple usage example:<br/>
以下是一个简单的使用示例：

```Python
import logop

logger = logop.Logging()
logger.info("Hello, world!")
logger.debug("This is a debug message.")  # This message will not be printed.
```

You can adjust the logger's log level and format.<br/>
您可以调整记录器的日志级别和格式。

```Python
logger.set_level(logop.DEBUG)
logger.set_format(logop.FORMAT_DEBUG)
```

Or set them on instantiation.<br/>
或者在实例化时设置它们。

```Python
logger = logop.Logging(level=logop.DEBUG, format=logop.FORMAT_DEBUG)
```

You can also write your own log format.<br/>
您还可以编写自己的日志格式。

```Python
logger.set_format("[$(.levelname)] $(.message)")
```


If you want to output a log with color,
then you need to refuse it to automaticallycreate a standard output object when creating logging. <br/>
如果你想输出带有颜色的日志，那么你需要拒绝它在创建日志记录器时自动创建一个标准输出对象。

Then add a better output object to it.<br/>
然后向其添加一个更好的输出对象。

```Python
logger = Logging(stdout=False)
logger.add_op(logop.LogopStandardPlus())
```

Or you want to output the log to the file.<br/>
或者您想将日志输出到文件。

```Python
fileobj = logop.LogopFile(directory="logs", filename="$(.date).log")
logger.add_op(fileobj)
```


### Advanced usage 高级用法

You can use custom levels and names to output logs<br/>
您可以使用自定义的级别和名称来输出日志。

```Python
logger.call(logop.DEBUG, "FINE", "This is a fine message.")
```

You can also add custom log levels to `LEVEL_TABLE` in the following format<br/>
您也可以按以下格式将自定义日志级别添加到 `LEVEL_TABLE` 中。

```Python
# ? LEVEL_TABLE[alias] = (level, level_name)
logop.LEVEL_TABLE["fine"] = (logop.DEBUG, "FINE")
```

Then you can use the alias as the attribute name to output the log directly in the logger.<br/>
然后你就可以使用别名作为属性名直接在日志记录器中输出日志。

```Python
logger.fine("This is a fine message.")
```

Add the `callabletrack` decorator to a function to track who calls the function,
the parameters provided and its return value.<br/>
为函数添加 `callabletrack` 装饰器可以追踪函数被谁调用、提供的参数及其返回值。

```Python
@logop.callabletrack
def test_func(a, b, c):
    ...
```

Set `exception` of `callabletrack` to `True` to log exception information.<br/>
将 `callabletrack` 的 `exception` 设置为 `True` 可以记录异常信息。

```Python
@logop.callabletrack(exception=True)
def test_func(a, b, c):
    ...
```


## Demo 演示

Output some simple log messages.<br/>
输出一些简单的日志消息。

![basic_log_output](image/log_output_basic.png)

Or output more detailed content.<br/>
或者输出更详细的内容。

![log_output_detailed](image/log_output_detailed.png)


Trace function calls and returns.<br/>
跟踪函数调用和返回。

![log_output_trace](image/call_trace.png)

Trace function exceptions.<br/>
跟踪函数异常。

![log_output_trace_exception](image/call_trace_exception.png)


I've provided some simple demo files. You can run them by executing the following command.<br/>
我提供了一些简单的演示文件。 您可以通过执行以下命令来运行它们。

```shell
python ./demo/demo_basic.py
python ./demo/demo_calleetrack.py
```


## Documentation 文档

Nothing<br/>
没写


## License 许可证

This project is licensed under the MIT License.<br/>
该项目使用 MIT 许可证。


</div>
