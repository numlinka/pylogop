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


@callabletrack
def demo_function(a: int, b: int) -> float:
    return a / b


def main():
    log.stdout.direct("\n")
    log.info("Let us first call the function in the right way.")
    demo_function(1, 1)

    try:
        log.stdout.direct("\n")
        log.info("Now let us call the function in the wrong way.")
        demo_function(1, 0)

    except ZeroDivisionError as _:
        ...


if __name__ == "__main__":
    main()
