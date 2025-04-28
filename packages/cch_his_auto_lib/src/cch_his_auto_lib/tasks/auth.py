import logging
import time
from contextlib import contextmanager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tasks import danhsachnguoibenhnoitru
from cch_his_auto_lib.helper import tracing, EndOfLoop

DEPT_DIALOG_CSS = ".ant-modal:has(.ant-modal-body>div>div>div>.ant-select)"
_logger = logging.getLogger().getChild("auth")
_trace = tracing(_logger)


@_trace
def login(driver: Driver, username: str, password: str):
    "login with provided `username` and `password`"
    URL = "http://emr.ndtp.org/login"
    _logger.info(f"login with username={username}")
    if not driver.current_url.startswith(URL):
        driver.goto(URL)
    for i in range(120):
        time.sleep(1)
        try:
            _logger.debug(f"waiting login page {i}...")
            driver.find(".login-body")
        except NoSuchElementException:
            try:
                _logger.debug("checking whether any user is logged in")
                driver.find(".card")
            except NoSuchElementException:
                _logger.debug("no user is currently logged in")
                continue
            else:
                _logger.info("found user already logged in -> proceed to log out")
                time.sleep(2)
                logout(driver)
                login(driver, username, password)
                return
        else:
            _logger.debug("found login screen")
            inputs = driver.find_elements(By.TAG_NAME, "input")
            time.sleep(2)  # wait for js to load
            _logger.debug("+++++ typing username and password")
            inputs[0].send_keys(username)
            inputs[1].send_keys(password)
            time.sleep(2)  # wait for js to load
            driver.clicking(".action>button", "submit button")
            driver.wait_closing(".login-body", "login page")
            return
    else:
        raise EndOfLoop("can't log in")


@_trace
def logout(driver: Driver):
    "logout, then back to login page"
    URL = "http://emr.ndtp.org/logout"
    driver.goto(URL)
    try:
        driver.waiting(".login-body")
        return
    except NoSuchElementException:
        logout(driver)


@_trace
def set_dept(driver: Driver, dept: str):
    "Set department with exact `dept`"
    _logger.info(f"dept={dept}")

    def _set_dept_in_dialog():
        ele = driver.waiting(
            f"{DEPT_DIALOG_CSS} input[type=search]", "dept dialog search input"
        )
        _logger.debug("+++++ typing dept")
        ActionChains(driver).send_keys_to_element(
            ele, Keys.ARROW_DOWN
        ).send_keys_to_element(ele, dept).send_keys_to_element(ele, Keys.ENTER).click(
            driver.find(f"{DEPT_DIALOG_CSS} .bottom-action .bottom-action-right button")
        ).perform()
        driver.wait_closing(DEPT_DIALOG_CSS, "dept dialog")

    for i in range(120):
        time.sleep(1)
        try:
            _logger.debug(f"waiting choose dept dialog {i}...")
            driver.find(f"{DEPT_DIALOG_CSS} input[type=search]")
        except NoSuchElementException:
            _logger.debug("-> can't find dept dialog")
            try:
                _logger.debug("checking whether dept is set")
                khoa = driver.find(".khoaLamViec div span")
            except NoSuchElementException:
                _logger.debug("-> can't find set dept, maybe the page is still loading")
                continue
            else:
                _logger.debug("-> found set dept, checking whether dept is set right")
                if not dept.strip().lower().startswith("khoa"):
                    dept = "khoa " + dept.strip().lower()
                if dept in khoa.text.strip().lower():
                    _logger.debug("-> dept is set right")
                    return
                else:
                    _logger.debug(
                        f"-> dept is not set to {dept} -> proceed to set dept"
                    )
                    driver.clicking2(".khoaLamViec div svg", "change dept button")
                    _set_dept_in_dialog()
                    return
        else:
            _logger.debug("-> found dept dialog")
            _set_dept_in_dialog()
            return
    else:
        raise EndOfLoop("can't set dept")


@contextmanager
def session(driver: Driver, username: str, password: str, dept: str):
    _logger.info("============start session============")
    login(driver, username, password)
    driver.goto(danhsachnguoibenhnoitru.URL)
    set_dept(driver, dept)
    try:
        yield driver
    finally:
        logout(driver)
        _logger.info("============end session============")
