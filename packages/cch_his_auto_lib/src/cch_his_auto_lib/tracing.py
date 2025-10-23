import logging
from logging import FileHandler
from typing import Callable

from rich.logging import RichHandler
from rich.console import Console


console = Console()

_rich = RichHandler(log_time_format="[%X]", show_path=False, console = console)
_rich.setFormatter(logging.Formatter(fmt="{name}:{message}", style="{"))
_rich.setLevel(logging.INFO)

_file = FileHandler("cch_his_auto_lib.log", mode="w")
_file.setFormatter(logging.Formatter(fmt="{name}-{levelname}: {message}", style="{"))
_file.setLevel(logging.DEBUG)

_root_lgr = logging.getLogger("lib")
_root_lgr.addHandler(_rich)
_root_lgr.addHandler(_file)


