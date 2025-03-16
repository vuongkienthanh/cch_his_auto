"""
### Tasks that are related to authentications
"""

import logging
import time

from selenium.webdriver.common.by import By

from cch_his_auto.driver import Driver

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
                _logger.info("found main screen")
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
