import logging
from logging import FileHandler
from typing import Callable

from rich.logging import RichHandler

_rich = RichHandler(log_time_format="[%X]")
_rich.setFormatter(logging.Formatter(fmt="{name}:{message}", style="{"))
_rich.setLevel(logging.INFO)

_file = FileHandler("cch_his_auto_lib.log", mode="w")
_file.setFormatter(logging.Formatter(fmt="{name}-{levelname}: {message}", style="{"))
_file.setLevel(logging.DEBUG)

_root_lgr = logging.getLogger("lib")
_root_lgr.addHandler(_rich)
_root_lgr.addHandler(_file)


def tracing(_lgr: logging.Logger) -> Callable:
    "Add logging to functions"

    def inner(f: Callable):
        def inner2(*args, **kwargs):
            name = f.__qualname__
            _lgr.debug(f"+++ start {name}")
            try:
                ret = f(*args, **kwargs)
            except Exception as e:
                _lgr.exception(f"??? error running {name}")
                raise e
            else:
                _lgr.info(f">>> finish {name}")
                return ret

        return inner2

    return inner
