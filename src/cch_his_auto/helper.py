import logging
import sys
from functools import wraps
import time

# set up logging
_logger = logging.getLogger()
_logger.setLevel(logging.INFO)
_out = logging.StreamHandler(sys.stdout)
_out.setFormatter(
    logging.Formatter(fmt="{asctime} {name} {levelname}: {message}", style="{")
)
_logger.addHandler(_out)

def tracing(logger: logging.Logger):
    def inner(f):
        @wraps(f)
        def inner2(*args, **kwargs):
            name = f.__qualname__
            logger.debug(f"+++ start {name}")
            try:
                f(*args, **kwargs)
            except Exception as e:
                logger.error(f"??? can't {name}: {e}")
                raise e
            else:
                logger.info(f">>> finish {name}")

        return inner2

    return inner
