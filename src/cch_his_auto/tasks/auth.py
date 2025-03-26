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
            _logger.info("found login screen")
            _logger.info("+++++ typing username and password")
            inputs = driver.find_elements(By.TAG_NAME, "input")
            inputs[0].send_keys(username)
            inputs[1].send_keys(password)
            time.sleep(2)
            driver.clicking(".action>button", "submit button")
            driver.waiting(".card", "main screen")
            break
        except:
            try:
                driver.find(".card")
                _logger.info("found main screen -> log out")
                logout(driver)
                break
            except:
                ...

def logout(driver: Driver):
    "logout `http://emr.bvndtp.org`, back to login page"
    driver.clicking(".header .header-icon:has(+.username)", "log info drop down")
    time.sleep(1)
    driver.clicking(".ant-popover .item-action:nth-child(3)", "logout")
    _logger.info("finish logout")
    driver.waiting(".login-body")

def choose_dept(driver: Driver, dept: str):
    "Choose department with exact `dept`"
    for _ in range(120):
        time.sleep(1)
        try:
            ele = driver.find(".ant-modal-body input")
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
            driver.waiting(".khoaLamViec div span")
            break
        except:
            try:
                khoa = driver.find(".khoaLamViec div span")
                if khoa.text.strip().lower() == dept.lower():
                    _logger.info("dept already set")
                    break
                else:
                    _logger.info(f"dept not set to {dept}")
                    driver.clicking(".khoaLamViec div span")
            except NoSuchElementException:
                ...

@contextmanager
def session(driver:Driver, username: str, password:str, dept:str):
    login(driver, username, password)
    driver.goto(danhsachnguoibenhnoitru.URL)
    choose_dept(driver, dept)
    try:
        yield driver
    finally:
        logout(driver)
