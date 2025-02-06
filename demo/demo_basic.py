# Licensed under the MIT License.
# logop by numlinka.
# demo

# std
import sys
sys.path.insert(0, "src")

# lib
from logop import *
from logop.constants import *


log = Logging(ALL, stdout=False)
log.add_stream(StandardOutputStreamPlus())

log.stdout.direct("\n")
log.trace("This is a trace message.")
log.debug("This is a debug message.")
log.info("This is an info message.")
log.warn("This is a warn message.")
log.warning("This is a warning message.")
log.error("This is an error message.")
log.severe("This is a severe message.")
log.critical("This is a critical message.")
log.fatal("This is a fatal message.")

log.set_format(FORMAT_TRACE)

log.stdout.direct("\n")
log.trace("This is a trace message.")
log.debug("This is a debug message.")
log.info("This is an info message.")
log.warn("This is a warn message.")
log.warning("This is a warning message.")
log.error("This is an error message.")
log.severe("This is a severe message.")
log.critical("This is a critical message.")
log.fatal("This is a fatal message.")
