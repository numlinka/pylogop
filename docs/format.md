# pylogop 日志格式

## 日志格式
```Python
logop.format.SIMPLE
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
| .mark      | $(.mark)      | 标记名称     | str      | initial       |

例: `"[$(.date) $(.time)] [$(.thread)/$(.levelname)] $(.message)"`
