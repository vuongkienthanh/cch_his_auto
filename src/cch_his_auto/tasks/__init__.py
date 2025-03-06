import logging
import time

from selenium.webdriver.common.by import By

from cch_his_auto.driver import Driver

logger = logging.getLogger()

def login(driver: Driver, username: str, password: str):
    URL = "http://emr.ndtp.org/login"
    if not driver.current_url.startswith(URL):
        driver.goto(URL)
    for _ in range(120):
        time.sleep(1)
        try:
            driver.finding(".login-body")
            logger.info("found login screen")
            logger.info("typing username and password")
            inputs = driver.find_elements(By.TAG_NAME, "input")
            inputs[0].send_keys(username)
            inputs[1].send_keys(password)
            time.sleep(2)
            driver.clicking(".action>button", "submit button")
            driver.waiting(".card", "main screen")
            break
        except:
            try:
                driver.finding(".card")
                logger.info("found main screen")
                break
            except:
                ...

def logout(driver: Driver):
    driver.clicking(".header .header-icon:has(+.username)")
    time.sleep(1)
    driver.clicking(".ant-popover .item-action:nth-child(2)")
    driver.waiting(".login-body")
