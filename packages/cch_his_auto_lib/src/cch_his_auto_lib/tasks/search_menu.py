import logging
import time

from selenium.webdriver import Keys
from cch_his_auto_lib.driver import Driver


_logger = logging.getLogger("search menu")

MENU_CSS = "div:has(>.ant-select~div>div>.ant-select-dropdown)"
MENU_SEARCH_CSS = f"{MENU_CSS} input[type=search]"
MENU_ITEMS_CSS = f"{MENU_CSS} .ant-select-dropdown"


def goto(driver: Driver, name: str):
    _logger.debug(f"filter with name= {name}")
    driver.waiting(f"{MENU_ITEMS_CSS} .ant-select-item", "menu item")
    search_bar = driver.clear_input(MENU_SEARCH_CSS)
    search_bar.send_keys(name)
    time.sleep(2)
    search_bar.send_keys(Keys.ENTER)
