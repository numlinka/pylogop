# Licensed under the MIT License.
# logop by numlinka.
# demo

# std
import sys
sys.path.insert(0, "src")

# lib
import logop
from logop.constants import *


logop.Logging(DEBUG, FORMAT.TRACE, stdout=False)
logop.ease.logging.add_stream(logop.StandardOutputStreamPlus())

logop.utils.add_log_level(WARN, "custom", "CUSTOM")
logop.utils.add_log_level(ERROR, "custom_2", "CUSTOM-2")

logop.ease.logging.custom("This is a custom log level.")
logop.ease.logging.custom_2("This is a custom_2 log level.")
