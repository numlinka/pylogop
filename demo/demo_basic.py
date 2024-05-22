# Licensed under the MIT License.
# logop by numlinka.
# demo

# std
import sys
sys.path.append("src")

# lib
from logop import *


logger = Logging(ALL, stdout=False)
logger.add_op(LogopStandardPlus())

sys.stdout.write("\n")
logger.trace("This is a trace message.")
logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warn("This is a warn message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.severe("This is a severe message.")
logger.critical("This is a critical message.")
logger.fatal("This is a fatal message.")

logger.set_format(FORMAT_DEBUG_EXTEND)

sys.stdout.write("\n")
logger.trace("This is a trace message.")
logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warn("This is a warn message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.severe("This is a severe message.")
logger.critical("This is a critical message.")
logger.fatal("This is a fatal message.")
