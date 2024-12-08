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


dict_1 = {1: "one", 2: "two", 3: "three"}

log.debug(dict_1)
log.debug(f"{dict_1}")
