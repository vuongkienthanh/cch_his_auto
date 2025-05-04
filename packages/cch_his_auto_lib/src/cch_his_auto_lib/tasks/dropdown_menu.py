from selenium.webdriver import ActionChains, Keys
from cch_his_auto_lib.driver import Driver


def close_dropdown(driver: Driver):
    ele = driver.waiting(".ant-select-dropdown", "dropdown")
    ActionChains(driver).send_keys_to_element(ele, Keys.ESCAPE).perform()


def count_item_dropdown(driver: Driver) -> int:
    driver.waiting(".ant-select-dropdown .ant-select-item", "dropdown")
    return len(driver.find_all(".ant-select-dropdown .ant-select-item"))


def select_item_dropdown(driver: Driver, i: int):
    driver.find_all(".ant-select-dropdown .ant-select-item")[i].click()
