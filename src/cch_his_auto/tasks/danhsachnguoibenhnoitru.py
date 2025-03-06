import logging
import time
import datetime as dt

from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from cch_his_auto.driver import Driver

logger = logging.getLogger()
URL = "http://emr.ndtp.org/quan-ly-noi-tru/danh-sach-nguoi-benh-noi-tru"
FMT = "%Y-%m-%d"

def filter_trangthainguoibenh(driver: Driver, row_indexes: list[int]):
    driver.clicking(
        ".base-search_component .ant-col:nth-child(7) button", "trang thai nguoi benh"
    )
    driver.waiting(".ant-popover label", "danh sach trang thai nguoi benh")
    logger.info("uncheck all boxes in trạng thái người bệnh")
    for ele in driver.findings(".ant-popover .ant-checkbox-checked"):
        ele.click()

    for i in row_indexes:
        driver.clicking(
            f".ant-popover label:nth-child({i}) .ant-checkbox",
            driver.finding(f".ant-popover label:nth-child({i})").text,
        )
    time.sleep(2)
    driver.clicking(
        ".base-search_component .ant-col:nth-child(7) button",
        "trang thai nguoi benh lan 2",
    )
    time.sleep(2)

def filter_thoigiannhapvien(driver: Driver, start: dt.date, end: dt.date):
    driver.clicking(".base-search_component .ant-col:nth-child(1) button", "Bộ lọc")
    driver.waiting(".date-1 .ant-picker-input input")
    logger.info("+++++ typing thoi gian vao khoa: start date & end date")
    ActionChains(driver).send_keys_to_element(
        driver.finding(".date-1 .ant-picker-input input"), start.strftime(FMT)
    ).pause(1).send_keys_to_element(
        driver.finding(".date-1 .ant-picker-input:nth-child(3) input"),
        end.strftime(FMT),
    ).send_keys(Keys.ENTER).perform()
    driver.clicking(".ant-popover .content-popover +div button", "Tìm button")
    time.sleep(2)

def filter_patient(driver: Driver, id: int) -> bool:
    ele = driver.clear_input(".base-search_component .ant-col:nth-child(2) input")
    logger.info(f"+++++ typing {id} to search entry")
    ele.send_keys(str(id))
    ele.send_keys(Keys.ENTER)
    time.sleep(2)
    try:
        driver.waiting_to_be(
            ".ant-table-body tbody tr:nth-child(2) td:nth-child(8)", str(id)
        )
        return True
    except:
        return False

def goto_patient(driver: Driver, id):
    if filter_patient(driver, id):
        driver.clicking(
            ".ant-table-body tbody tr:nth-child(2) td:nth-child(30)",
            "first row",
        )
        driver.waiting_to_be(
            ".patient-information .ant-row span:nth-child(2) b", str(id)
        )
        time.sleep(2)
