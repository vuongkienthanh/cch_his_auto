"""
### Tasks that are related to authentications
"""

import logging
import time
from contextlib import contextmanager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import NoSuchElementException

from cch_his_auto.driver import Driver
from cch_his_auto.tasks import danhsachnguoibenhnoitru

_logger = logging.getLogger().getChild("tasks").getChild("auth")

def login(driver: Driver, username: str, password: str):
    "login with provided `username` and `password`"
    URL = "http://emr.ndtp.org/login"
    if not driver.current_url.startswith(URL):
        driver.goto(URL)
    for i in range(120):
        time.sleep(1)
        _logger.debug(f"waiting login page {i}...")
        try:
            driver.find(".login-body")
        except NoSuchElementException:
            try:
                _logger.debug("checking whether any user is logged in")
                driver.find(".card")
            except NoSuchElementException:
                _logger.debug("no user is currently logged in")
                continue
            else:
                _logger.debug("found user already logged in -> proceed to log out")
                time.sleep(2)
                logout(driver)
        else:
            _logger.debug("found login screen")
            inputs = driver.find_elements(By.TAG_NAME, "input")
            time.sleep(3)  # wait for js to load
            inputs[0].send_keys(username)
            inputs[1].send_keys(password)
            driver.clicking(".action>button", "submit button")
            driver.waiting(".card", "main screen")
            _logger.info(f"+++++ log in success: {username}")
            return
    else:
        _logger.error("can't login")
        raise Exception("can't login")

def logout(driver: Driver):
    "logout, then back to login page"
    time.sleep(5)  # wait for it to be dropdown-able
    for i in range(5):
        time.sleep(1)
        _logger.debug(f"trying logout {i}...")
        driver.clicking(".header .header-icon:has(+.username)", "log info drop down")
        try:
            driver.clicking(".ant-popover .item-action:last-child", "logout")
        except:
            continue
        else:
            driver.waiting(".login-body")
            _logger.debug("logged out")
            return
    else:
        _logger.error("can't logout")
        raise Exception("can't logout")

def choose_dept(driver: Driver, dept: str):
    "Choose department with exact `dept`"
    for i in range(120):
        time.sleep(1)
        _logger.debug(f"waiting choose dept dialog {i}...")
        try:
            driver.find(".ant-modal-body input[type=search]")
        except NoSuchElementException:
            try:
                _logger.debug("checking whether dept is set")
                khoa = driver.find(".khoaLamViec div span")
            except NoSuchElementException:
                _logger.debug("can't find set dept, maybe the page is still loading")
                continue
            else:
                _logger.debug("found set dept, checking whether dept is set right")
                if not dept.strip().lower().startswith("khoa"):
                    dept = "khoa " + dept.strip().lower()
                if dept in khoa.text.strip().lower():
                    _logger.info(f"->dept is set: {dept}")
                    return
                else:
                    _logger.debug(f"dept is not set to {dept} -> proceed to set dept")
                    _set_dept_in_dialog(driver, dept)
                    return
        else:
            _logger.debug("found dept picker")
            _set_dept_in_dialog(driver, dept)
            return
    else:
        _logger.error("can't set dept")
        raise Exception("can't set dept")

def _set_dept_in_dialog(driver: Driver, dept: str):
    ele = driver.waiting(".ant-modal-body input[type=search]", "dept picker")
    ActionChains(driver).send_keys_to_element(
        ele, Keys.ARROW_DOWN
    ).send_keys_to_element(ele, dept).send_keys_to_element(ele, Keys.ENTER).click(
        driver.find(".ant-modal-body .bottom-action .bottom-action-right button")
    ).perform()
    driver.waiting(".khoaLamViec div span", "dept info")
    _logger.info(f"dept is set: {dept}")

@contextmanager
def session(driver: Driver, username: str, password: str, dept: str):
    login(driver, username, password)
    driver.goto(danhsachnguoibenhnoitru.URL)
    choose_dept(driver, dept)
    try:
        yield driver
    finally:
        logout(driver)
