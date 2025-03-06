import logging
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import NoSuchElementException, StaleElementReferenceException

from cch_his_auto.driver import Driver

logger = logging.getLogger()

def choose_dept(driver: Driver, dept: str):
    for _ in range(120):
        time.sleep(1)
        try:
            ele = driver.finding(".ant-modal-body input")
            logger.info("found dept picker")
            ActionChains(driver).send_keys_to_element(
                ele, Keys.ARROW_DOWN
            ).send_keys_to_element(ele, dept).send_keys_to_element(
                ele, Keys.ENTER
            ).click(
                driver.finding(
                    ".ant-modal-body .bottom-action .bottom-action-right button"
                )
            ).perform()
            break
        except:
            try:
                ele = driver.finding(".khoaLamViec div span")
                if ele.text.strip() == dept:
                    logger.info("dept already set")
                    break
                else:
                    logger.info(f"dept not set to {dept}")
                    driver.clicking(".khoaLamViec div span")
            except NoSuchElementException:
                ...

def click_sign_btn(
    driver: Driver, pre_btn_css: str, post_btn_css: str, post_btn_text: str
):
    driver.clicking(pre_btn_css, "clicking Ký tên")
    for _ in range(120):
        time.sleep(1)
        try:
            if driver.finding(post_btn_css).text.strip() == post_btn_text:
                break
        except (NoSuchElementException, StaleElementReferenceException):
            break
    time.sleep(2)
