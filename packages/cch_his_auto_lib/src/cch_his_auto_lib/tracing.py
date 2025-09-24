import logging
from typing import Callable
import sys

_out = logging.StreamHandler(sys.stdout)
_out.setFormatter(
    logging.Formatter(fmt="{asctime} {name} {levelname}: {message}", style="{")
)


def enter():
    global _out
    root_logger = logging.getLogger()
    root_logger.addHandler(_out)
    return _out


def close():
    global _out
    root_logger = logging.getLogger()
    root_logger.removeHandler(_out)


def tracing(logger: logging.Logger) -> Callable:
    "Add logging to functions"

    def inner(f: Callable):
        def inner2(*args, **kwargs):
            name = f.__qualname__
            logger.debug(f"+++ start {name}")
            try:
                ret = f(*args, **kwargs)
            except:
                logger.error(f"??? error running {name}")
                raise
            else:
                logger.info(f">>> finish {name}")
                return ret

        return inner2

    return inner
