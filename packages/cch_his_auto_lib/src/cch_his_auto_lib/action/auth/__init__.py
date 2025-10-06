import time
import logging
from contextlib import contextmanager

from rich import print

from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.errors import TaskUncompleteException, WaitClosingException
from cch_his_auto_lib.tracing import tracing
from cch_his_auto_lib.action import danhsachnguoibenhnoitru

_lgr = logging.getLogger("auth")
_trace = tracing(_lgr)


from . import dept_dialog


LOGIN_PANE_CSS = ".login-body"


@_trace
def login(d: Driver, username: str, password: str):
    "login with provided `username` and `password`"
    URL = "http://emr.ndtp.org/login"
    _lgr.info(f"login with username={username}")
    if not d.current_url.startswith(URL):
        d.goto(URL)
    for i in range(120):
        time.sleep(1)
        try:
            _lgr.debug(f"waiting login page {i}...")
            d.find(LOGIN_PANE_CSS)
        except NoSuchElementException:
            try:
                _lgr.debug("checking whether any user is logged in")
                d.find(".card")
            except NoSuchElementException:
                _lgr.debug("no user is currently logged in")
                continue
            else:
                _lgr.info("found user already logged in -> proceed to log out")
                time.sleep(2)
                logout(d)
                login(d, username, password)
                return
        else:
            _lgr.debug("found login screen")
            inputs = d.find_elements(By.TAG_NAME, "input")
            time.sleep(2)  # wait for js to load
            _lgr.debug("+++++ typing username and password")
            inputs[0].send_keys(username)
            inputs[1].send_keys(password)
            time.sleep(5)  # wait for js to load
            d.clicking(".action>button", "submit button")
            try:
                d.wait_closing(LOGIN_PANE_CSS, "login page")
            except WaitClosingException:
                # one more time, cuz sometimes submit button doesn't work
                d.clicking(".action>button", "submit button")
                d.wait_closing(LOGIN_PANE_CSS, "login page")
            return
    else:
        raise TaskUncompleteException("can't log in")


@_trace
def logout(d: Driver):
    "logout, then back to login page"
    URL = "http://emr.ndtp.org/logout"
    d.goto(URL)
    try:
        d.waiting(LOGIN_PANE_CSS)
        return
    except NoSuchElementException:
        logout(d)


@_trace
def set_dept(d: Driver, dept: str):
    "Set department with exact `dept`"
    _lgr.info(f"dept={dept}")

    def _set_dept_in_dialog():
        dept_dialog.filter(d, dept)
        dept_dialog.select_item_dropdown(d, 0)
        dept_dialog.save(d)

    for i in range(120):
        time.sleep(1)
        try:
            _lgr.debug(f"waiting choose dept dialog {i}...")
            d.find(dept_dialog.DIALOG_CSS)
        except NoSuchElementException:
            _lgr.debug("-> can't find dept dialog")
            try:
                _lgr.debug("checking whether dept is set")
                khoalamviec = d.find(".khoaLamViec div span")
            except NoSuchElementException:
                _lgr.debug("-> can't find set dept, maybe the page is still loading")
                continue
            else:
                _lgr.debug("-> found set dept, checking whether dept is set right")
                if dept in khoalamviec.text.strip().lower():
                    _lgr.info("-> dept is set right")
                    return
                else:
                    _lgr.info(f"-> dept is not set to {dept} -> proceed to set dept")
                    d.clicking2(".khoaLamViec div svg", "change dept button")
                    _set_dept_in_dialog()
                    return
        else:
            _lgr.debug("-> found dept dialog")
            _set_dept_in_dialog()
            return
    else:
        raise TaskUncompleteException("can't set dept")


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
