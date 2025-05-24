import logging
import time
from contextlib import contextmanager

from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.tasks import danhsachnguoibenhnoitru, search_dialog
from cch_his_auto_lib.helper import tracing, EndOfLoop

_lgr = logging.getLogger().getChild("auth")
_trace = tracing(_lgr)

LOGIN_PANE_CSS = ".login-body"


@_trace
def login(username: str, password: str):
    "login with provided `username` and `password`"
    _d = get_global_driver()
    URL = "http://emr.ndtp.org/login"
    _lgr.info(f"login with username={username}")
    if not _d.current_url.startswith(URL):
        _d.goto(URL)
    for i in range(120):
        time.sleep(1)
        try:
            _lgr.debug(f"waiting login page {i}...")
            _d.find(LOGIN_PANE_CSS)
        except NoSuchElementException:
            try:
                _lgr.debug("checking whether any user is logged in")
                _d.find(".card")
            except NoSuchElementException:
                _lgr.debug("no user is currently logged in")
                continue
            else:
                _lgr.info("found user already logged in -> proceed to log out")
                time.sleep(2)
                logout()
                login(username, password)
                return
        else:
            _lgr.debug("found login screen")
            inputs = _d.find_elements(By.TAG_NAME, "input")
            time.sleep(2)  # wait for js to load
            _lgr.debug("+++++ typing username and password")
            inputs[0].send_keys(username)
            inputs[1].send_keys(password)
            time.sleep(2)  # wait for js to load
            _d.clicking(".action>button", "submit button")
            _d.wait_closing(LOGIN_PANE_CSS, "login page")
            return
    else:
        raise EndOfLoop("can't log in")


@_trace
def logout():
    "logout, then back to login page"
    _d = get_global_driver()
    URL = "http://emr.ndtp.org/logout"
    _d.goto(URL)
    try:
        _d.waiting(LOGIN_PANE_CSS)
        return
    except NoSuchElementException:
        logout()


@_trace
def set_dept(dept: str):
    "Set department with exact `dept`"
    _lgr.info(f"dept={dept}")
    _d = get_global_driver()

    def _set_dept_in_dialog():
        search_dialog.filter(dept)
        search_dialog.select_item_dropdown(0)
        search_dialog.save()

    for i in range(120):
        time.sleep(1)
        try:
            _lgr.debug(f"waiting choose dept dialog {i}...")
            _d.find(search_dialog.DIALOG_CSS)
        except NoSuchElementException:
            _lgr.debug("-> can't find dept dialog")
            try:
                _lgr.debug("checking whether dept is set")
                khoalamviec = _d.find(".khoaLamViec div span")
            except NoSuchElementException:
                _lgr.debug("-> can't find set dept, maybe the page is still loading")
                continue
            else:
                _lgr.debug("-> found set dept, checking whether dept is set right")
                if not (dept := dept.strip().lower()).startswith("khoa"):
                    dept = "khoa " + dept
                if dept in khoalamviec.text.strip().lower():
                    _lgr.info("-> dept is set right")
                    return
                else:
                    _lgr.info(f"-> dept is not set to {dept} -> proceed to set dept")
                    _d.clicking2(".khoaLamViec div svg", "change dept button")
                    _set_dept_in_dialog()
                    return
        else:
            _lgr.debug("-> found dept dialog")
            _set_dept_in_dialog()
            return
    else:
        raise EndOfLoop("can't set dept")


@contextmanager
def session(username: str, password: str, dept: str):
    _lgr.info("============start session============")
    _d = get_global_driver()
    login(username, password)
    _d.goto(danhsachnguoibenhnoitru.URL)
    set_dept(dept)
    try:
        yield
    finally:
        logout()
        _lgr.info("============end session============")
