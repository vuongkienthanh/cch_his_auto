from contextlib import contextmanager

from rich import print

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action import danhsachnguoibenhnoitru
from cch_his_auto_lib.action.auth import login, logout, set_dept


@contextmanager
def session(d: Driver, username: str, password: str, dept: str):
    print("[red]============start session============")
    login(d, username, password)
    d.goto(danhsachnguoibenhnoitru.URL)
    set_dept(d, dept)
    try:
        yield
    finally:
        logout(d)
        print("[red]============end session============")
