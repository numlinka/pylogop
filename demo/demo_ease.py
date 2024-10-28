# Licensed under the MIT License.
# logop by numlinka.
# demo

# std
import sys
sys.path.insert(0, "src")

# lib
import logop

logop.ease.logging.set_format(logop.constants.FORMAT.TRACE)


logop.info("Hello, World!")
