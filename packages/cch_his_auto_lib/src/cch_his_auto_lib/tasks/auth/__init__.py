from contextlib import contextmanager
import logging


from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tasks import danhsachnguoibenhnoitru
from cch_his_auto_lib.tracing import tracing
from .welcome import login, logout, set_dept

_lgr = logging.getLogger("auth")
_trace = tracing(_lgr)


@contextmanager
def session(d: Driver, username: str, password: str, dept: str):
    _lgr.info("============start session============")
    login(d, username, password)
    d.goto(danhsachnguoibenhnoitru.URL)
    set_dept(d, dept)
    try:
        yield
    finally:
        logout(d)
        _lgr.info("============end session============")
