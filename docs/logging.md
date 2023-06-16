# pylogop 日志管理器

日志管理器可以添加和删除日志输出对象，并根据日志级别过滤日志消息。它还支持异步日志记录，可以在后台线程中处理日志消息，以提高性能。

日志管理器负责收集日志信息并将数据传递给日志输出对象，由日志输出对象进行输出


## Logging 日志管理器

```Python
logop.Logging(level: int = INFO, op_format: str = FORMAT.DEFAULT, *, stdout: bool = True,
              asynchronous: bool = False, threadname: str = 'LoggingThread')
# 初始化一个日志对象
# level: 日志等级, 低于这个等级的日志不会被显示/输出, 建议通过日志等级常量设置.
# op_format: 日志格式, 日志消息的组合方式, 输出对象不一定会遵守这个格式.
# stdout: 是否自动初始化一个标准输出对象.
# asynchronous: 创建一个线程让日志对象异步执行.
# threadname: 线程名称, 仅在 asynchronous 为 True 时生效.


.set_level(level: int | str) -> None
# 设置日志等级
# 低于这个等级的日志不会被显示/输出, 可以通过日志等级常量设置.
# 也可以通过日志等级别名设置, 这个别名必须是存在于 levelTable 中的.

.set_format(op_format: str) -> None
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

.join(timeout: float | None = None) -> None
# 等待日志记录器线程结束
# 仅在异步模式下有效, 否则抛出 RuntimeError 异常.
# timeout: 超时时间, 单位为秒.

.close() -> None
# 关闭日志记录器
# 关闭之后日志记录器不再可用.

.is_close() -> bool
# 日志记录器是否已被关闭

.call(level: int = INFO, levelname: str = 'INFO', message: str = '', mark: str = "",
      *, double_back: bool = False) -> None
# 输出日志
# level: 日志等级, 当等级低于设置等级时不进行日志输出.
# levelname: 日志名称, 任意, 但推荐为 INFO, WARN, ERROR, DEBUG 等标准名称.
# message: 日志消息.
# mark: 额外标记名称 ( 扩展内容 ), 默认日志格式不会输出这项信息
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
