import logging
import sys
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


_iframe_logger = _logger.getChild("iframe")


@contextmanager
def iframe(driver: "driver.Driver", iframe_css: str):
    "use as contextmanager for going in and out an iframe inside a modal"
    try:
        _iframe_logger.debug("go into iframe")
        iframe = driver.waiting(iframe_css)
        driver.switch_to.frame(iframe)
        yield iframe
    finally:
        _iframe_logger.debug("go back to parent frame")
        driver.switch_to.parent_frame()
