# Licensed under the MIT License.
# logop by numlinka.
# demo

# std
import sys
sys.path.insert(0, "src")

# lib
from logop import *
from logop.constants import *


logger = Logging(ALL, stdout=False)
logger.add_stream(StandardOutputStreamPlus())

logger.stdout.direct("\n")
logger.trace("This is a trace message.")
logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warn("This is a warn message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.severe("This is a severe message.")
logger.critical("This is a critical message.")
logger.fatal("This is a fatal message.")

logger.set_format(FORMAT.TRACE)

logger.stdout.direct("\n")
logger.trace("This is a trace message.")
logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warn("This is a warn message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.severe("This is a severe message.")
logger.critical("This is a critical message.")
logger.fatal("This is a fatal message.")
