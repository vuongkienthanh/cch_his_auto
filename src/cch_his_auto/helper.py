import logging
import sys
from functools import wraps
from contextlib import contextmanager

from . import driver

# set up logging
_logger = logging.getLogger()
_out = logging.StreamHandler(sys.stdout)
_out.setFormatter(
    logging.Formatter(fmt="{asctime} {name} {levelname}: {message}", style="{")
)
_logger.addHandler(_out)


def tracing(logger: logging.Logger):
    "Add logging capability to `DriverFn`"

    def inner(f: "driver.DriverFn"):
        @wraps(f)
        def inner2(*args, **kwargs):
            name = f.__qualname__
            logger.debug(f"+++ start {name}")
            try:
                f(*args, **kwargs)
            except Exception as e:
                logger.error(f"??? error running {name}: {e}")
                raise e
            else:
                logger.info(f">>> finish {name}")

        return inner2

    return inner


class EndOfLoop(Exception):
    def __init__(self, *args):
        super().__init__(*args)


@contextmanager
def iframe(driver: "driver.Driver", iframe_css: str, /, logger: logging.Logger | None):
    "use as contextmanager for going in and out an iframe inside a modal"
    if logger is None:
        logger = logging.getLogger()
    try:
        logger.debug("go into iframe")
        iframe = driver.waiting(iframe_css)
        driver.switch_to.frame(iframe)
        yield iframe
    finally:
        logger.debug("go back to parent frame")
        driver.switch_to.parent_frame()
