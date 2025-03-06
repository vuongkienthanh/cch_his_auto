import time
import logging
from functools import partial

from selenium.webdriver import Keys
from selenium.common import NoSuchElementException

from cch_his_auto.driver import Driver, DriverFn
from cch_his_auto.tasks import raw_page_sign_name as s
from cch_his_auto.tasks.common import click_sign_btn

logger = logging.getLogger()

def start(driver: Driver):
    driver.clicking(
        ".thong-tin-benh-nhan .bunch-icon div:nth-child(3)", "xem ho so benh an"
    )
    driver.waiting(".right-content tbody tr:nth-child(2) ", "Danh sách phiếu")
    time.sleep(2)

def close(driver: Driver):
    driver.clicking(".ant-modal button[aria-label='Close']", "close button")
    driver.waiting(
        ".thong-tin-benh-nhan .bunch-icon div:nth-child(3)", "close ho so benh an"
    )
    time.sleep(5)

def filter(driver: Driver, name: str) -> bool:
    ele = driver.clear_input(".right-content .header input")
    time.sleep(2)
    logger.info(f"typing {name}")
    ele.send_keys(name)
    ele.send_keys(Keys.ENTER)
    for _ in range(20):
        time.sleep(1)
        try:
            ele = driver.finding(
                ".right-content tbody tr:nth-child(2) td:nth-child(2) div"
            )
            if ele.text.strip().startswith(name):
                logger.error("filtered with result found")
                return True
        except NoSuchElementException:
            pass
    else:
        logger.error("filtered with no result")
        return False

def is_row_hoanthanh(driver: Driver, idx: int) -> bool:
    ele = driver.waiting(f".ant-table-tbody tr:nth-child({idx}) td:nth-child(3)")
    name = driver.waiting(f".ant-table-tbody tr:nth-child({idx}) td:nth-child(2)").text
    logger.info(f"checking {name}: Hoan thanh")
    return ele.text.strip() != "Chưa ký"

def is_row_expandable(driver: Driver, idx: int) -> bool:
    name = driver.waiting(f".ant-table-tbody tr:nth-child({idx}) td:nth-child(2)").text
    logger.info(f"checking {name}: expandable")
    time.sleep(1)
    try:
        ele = driver.finding(
            f".right-content tbody tr:nth-child({idx}) td:nth-child(1) button"
        )
    except:
        return False
    class_list = ele.get_attribute("class")
    assert class_list is not None
    return "ant-table-row-expand-icon-collapsed" in class_list

def expand_row(driver: Driver, idx: int):
    name = driver.waiting(f".ant-table-tbody tr:nth-child({idx}) td:nth-child(2)").text
    logger.info(f"expanding {name}")
    driver.clicking(f".right-content tbody tr:nth-child({idx}) td:nth-child(1) button")

def sign_new_tab(driver: Driver, idx: int, sign_fn: DriverFn):
    tab0 = driver.current_window_handle
    datakey = driver.finding(f".ant-table-tbody tr:nth-child({idx})").get_attribute(
        "data-row-key"
    )
    logger.info(f"data row key = {datakey}")
    driver.clicking(f".ant-table-tbody tr:nth-child({idx})", f"row {idx - 1}")
    time.sleep(2)
    driver.clicking(f"a[data-key='{datakey}'] button", f"edit button {idx - 1}")
    driver.goto_newtab_do_smth_then_goback(tab0, sign_fn)

def sign_current(driver: Driver):
    click_sign_btn(
        driver,
        ".right-content .__action button:nth-child(2)",
        ".right-content .__action button:nth-child(2)",
        "Hủy ký Bác sĩ",
    )

def filter_check_expand_sign_curent(driver: Driver, name: str):
    if filter(driver, name):
        if is_row_expandable(driver, 2):
            expand_row(driver, 2)
            for i in range(3, len(driver.findings("tbody .ant-table-row-level-1")) + 3):
                if not is_row_hoanthanh(driver, i):
                    logger.info("hoan thanh: no")
                    driver.clicking(f"tbody tr:nth-child({i})")
                    time.sleep(1)
                    sign_current(driver)
                else:
                    logger.info("hoan thanh: yes")
        else:
            if not is_row_hoanthanh(driver, 2):
                driver.clicking("tbody tr:nth-child(2)")
                logger.info("hoan thanh: no")
                sign_current(driver)
            else:
                logger.info("hoan thanh: yes")
    time.sleep(3)

def filter_check_expand_sign_new_tab(driver: Driver, name: str, sign_fn: DriverFn):
    if filter(driver, name):
        if is_row_expandable(driver, 2):
            expand_row(driver, 2)
            for i in range(3, len(driver.findings("tbody .ant-table-row-level-1")) + 3):
                if not is_row_hoanthanh(driver, i):
                    logger.info("hoan thanh: no")
                    driver.clicking(f"tbody tr:nth-child({i})")
                    time.sleep(1)
                    sign_new_tab(driver, i, sign_fn)
                else:
                    logger.info("hoan thanh: yes")
        else:
            if not is_row_hoanthanh(driver, 2):
                logger.info("hoan thanh: no")
                sign_new_tab(driver, 2, sign_fn)
            else:
                logger.info("hoan thanh: yes")
    time.sleep(3)

tobiabenhannhikhoa = partial(
    filter_check_expand_sign_new_tab,
    name="Tờ bìa bệnh án Nhi khoa",
    sign_fn=s.tobiabenhannhikhoa,
)
mucAbenhannhikhoa = partial(
    filter_check_expand_sign_new_tab,
    name="Mục A - Bệnh án Nhi khoa",
    sign_fn=s.mucAbenhannhikhoa,
)
mucBtongketbenhan = partial(
    filter_check_expand_sign_new_tab,
    name="Mục B - Tổng kết Bệnh án (Nội khoa, Nhi Khoa, Truyền nhiễm, Sơ sinh, Da liễu, DD-PHCN, HHTM)",
    sign_fn=s.mucBtongketbenhan,
)

phieuchidinhxetnghiem = partial(
    filter_check_expand_sign_curent,
    name="Phiếu chỉ định xét nghiệm",
)

todieutri = partial(
    filter_check_expand_sign_new_tab,
    name="Tờ điều trị",
    sign_fn=s.todieutri,
)
