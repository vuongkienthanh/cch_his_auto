import logging
from typing import Callable


def tracing(logger: logging.Logger):
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


class EndOfLoop(Exception):
    "Loop checking css element but not found"
