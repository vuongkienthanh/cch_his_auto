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

_logger = logging.getLogger()

def login(driver: Driver, username: str, password: str):
    "login to `http://emr.bvndtp.org`, with provided `username` and `password`"
    URL = "http://emr.ndtp.org/login"
    if not driver.current_url.startswith(URL):
        driver.goto(URL)
    for _ in range(120):
        time.sleep(1)
        try:
            driver.find(".login-body")
        except NoSuchElementException:
            try:
                driver.find(".card")
            except NoSuchElementException:
                continue
            else:
                _logger.info("found main screen -> log out")
                time.sleep(2)
                logout(driver)
        else:
            _logger.info("found login screen")
            _logger.info("+++++ typing username and password")
            inputs = driver.find_elements(By.TAG_NAME, "input")
            time.sleep(5)  # wait for js to load
            inputs[0].send_keys(username)
            inputs[1].send_keys(password)
            driver.clicking(".action>button", "submit button")
            driver.waiting(".card", "main screen")
            return
    else:
        raise Exception("can't login")

def logout(driver: Driver):
    "logout `http://emr.bvndtp.org`, back to login page"
    time.sleep(5)  # wait for it to be dropdown-able
    for _ in range(5):
        driver.clicking(".header .header-icon:has(+.username)", "log info drop down")
        time.sleep(1)
        try:
            driver.clicking(".ant-popover .item-action:last-child", "logout")
        except:
            continue
        else:
            driver.waiting(".login-body")
            return
    else:
        raise Exception("can't logout")

def choose_dept(driver: Driver, dept: str):
    "Choose department with exact `dept`"
    for _ in range(120):
        time.sleep(1)
        try:
            ele = driver.find(".ant-modal-body input[type=search]")
        except NoSuchElementException:
            try:
                khoa = driver.find(".khoaLamViec div span")
            except NoSuchElementException:
                continue
            else:
                if not dept.strip().lower().startswith("khoa"):
                    dept = "khoa " + dept.strip().lower()
                if dept in khoa.text.strip().lower():
                    _logger.info("dept already set")
                    break
                else:
                    _logger.info(f"dept not set to {dept}")
                    driver.clicking(".khoaLamViec div span")
        else:
            _logger.info("found dept picker")
            ActionChains(driver).send_keys_to_element(
                ele, Keys.ARROW_DOWN
            ).send_keys_to_element(ele, dept).send_keys_to_element(
                ele, Keys.ENTER
            ).click(
                driver.find(
                    ".ant-modal-body .bottom-action .bottom-action-right button"
                )
            ).perform()
            driver.waiting(".khoaLamViec div span", "dept being set")
            break
    else:
        raise Exception("can't set dept")

@contextmanager
def session(driver: Driver, username: str, password: str, dept: str):
    login(driver, username, password)
    driver.goto(danhsachnguoibenhnoitru.URL)
    choose_dept(driver, dept)
    try:
        yield driver
    finally:
        logout(driver)
