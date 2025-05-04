from selenium.webdriver import ActionChains, Keys
from cch_his_auto_lib.driver import Driver

DROPDOWN_CSS = ".ant-select-dropdown:not(.ant-select-dropdown-hidden)"


def close_dropdown(driver: Driver):
    ele = driver.waiting(DROPDOWN_CSS, "dropdown")
    ActionChains(driver).send_keys_to_element(ele, Keys.ESCAPE).perform()


def count_item_dropdown(driver: Driver) -> int:
    driver.waiting(f"{DROPDOWN_CSS} .ant-select-item", "dropdown")
    return len(driver.find_all(f"{DROPDOWN_CSS} .ant-select-item"))


def select_item_dropdown(driver: Driver, i: int):
    driver.find_all(f"{DROPDOWN_CSS} .ant-select-item")[i].click()
