# Licensed under the MIT License.
# logop by numlinka.
# demo

# std
import sys
sys.path.insert(0, "src")

# lib
import logop
from logop.constants import *


log = logop.Logging(DEBUG, FORMAT_TRACE, stdout=False)
stdout = logop.StandardOutputStreamPlus()
log.add_stream(stdout)

logop.utils.add_log_level(WARN, "custom", "CUSTOM")
logop.utils.add_log_level(ERROR, "custom_2", "CUSTOM-2")

log.custom("This is a custom log level.")
log.custom_2("This is a custom_2 log level.")

stdout.set_level_color(WARN, ITALIC, FG_YELLOW)

log.warn("This is a warn message.")
