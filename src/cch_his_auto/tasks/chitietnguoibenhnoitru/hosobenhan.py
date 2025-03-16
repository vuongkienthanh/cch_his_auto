"""
### Tasks that operate on *Hồ sơ bệnh án*
###### inside "*Chi tiết người bệnh nội trú*
"""

import time
import logging

from selenium.webdriver import Keys
from selenium.common import NoSuchElementException, StaleElementReferenceException

from cch_his_auto.driver import Driver, DriverFn
from cch_his_auto.tasks.editor import sign_staff_name as e

_logger = logging.getLogger()

def open(driver: Driver):
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
    "Filter document based on `name`"
    ele = driver.clear_input(".right-content .header input")
    time.sleep(2)
    _logger.info(f"typing {name}")
    ele.send_keys(name)
    ele.send_keys(Keys.ENTER)
    for _ in range(20):
        time.sleep(1)
        try:
            ele = driver.find(
                ".right-content tbody tr:nth-child(2) td:nth-child(2) div"
            )
            if ele.text.strip().startswith(name):
                _logger.info(f"found {name}")
                return True
        except NoSuchElementException:
            pass
    else:
        _logger.error("filtered with no result")
        return False

def is_row_hoanthanh(driver: Driver, idx: int) -> bool:
    "Check if row at `idx` is *Hoàn thành*, first row is id=2"
    ele = driver.waiting(f".ant-table-tbody tr:nth-child({idx}) td:nth-child(3)")
    name = driver.waiting(f".ant-table-tbody tr:nth-child({idx}) td:nth-child(2)").text
    _logger.info(f"checking {name}: Hoan thanh")
    return ele.text.strip() == "Hoàn thành"

def is_row_dangky(driver: Driver, idx: int) -> bool:
    "Check if row at `idx` is *Đang ký*, first row is id=2"
    ele = driver.waiting(f".ant-table-tbody tr:nth-child({idx}) td:nth-child(3)")
    name = driver.waiting(f".ant-table-tbody tr:nth-child({idx}) td:nth-child(2)").text
    _logger.info(f"checking {name}: Dang ky")
    return ele.text.strip() == "Đang ký"

def is_row_chuaky(driver: Driver, idx: int) -> bool:
    "Check if row at `idx` is *Chưa ký*, first row is id=2"
    ele = driver.waiting(f".ant-table-tbody tr:nth-child({idx}) td:nth-child(3)")
    name = driver.waiting(f".ant-table-tbody tr:nth-child({idx}) td:nth-child(2)").text
    _logger.info(f"checking {name}: Chua ky")
    return ele.text.strip() == "Chưa ký"

def is_row_expandable(driver: Driver, idx: int) -> bool:
    "Check if row at `idx` is expandable, first row is id=2"
    name = driver.waiting(f".ant-table-tbody tr:nth-child({idx}) td:nth-child(2)").text
    _logger.info(f"checking {name}: expandable")
    time.sleep(1)
    try:
        ele = driver.find(
            f".right-content tbody tr:nth-child({idx}) td:nth-child(1) button"
        )
    except:
        return False
    class_list = ele.get_attribute("class")
    assert class_list is not None
    return "ant-table-row-expand-icon-collapsed" in class_list

def expand_row(driver: Driver, idx: int):
    "Expand row at `idx`"
    name = driver.waiting(f".ant-table-tbody tr:nth-child({idx}) td:nth-child(2)").text
    _logger.info(f"expanding {name}")
    driver.clicking(f".right-content tbody tr:nth-child({idx}) td:nth-child(1) button")

def sign_new_tab(driver: Driver, idx: int, sign_fn: DriverFn):
    "@private"
    tab0 = driver.current_window_handle
    datakey = driver.find(f".ant-table-tbody tr:nth-child({idx})").get_attribute(
        "data-row-key"
    )
    _logger.info(f"data row key = {datakey}")
    driver.clicking(f".ant-table-tbody tr:nth-child({idx})", f"row {idx - 1}")
    time.sleep(2)
    driver.clicking(f"a[data-key='{datakey}'] button", f"edit button {idx - 1}")
    driver.goto_newtab_do_smth_then_goback(tab0, sign_fn)

def sign_current(driver: Driver):
    "@private"
    driver.clicking(".right-content .__action button:nth-child(2)", "clicking Ký tên")
    for _ in range(120):
        time.sleep(1)
        try:
            if (
                driver.find(".right-content .__action button:nth-child(2)").text.strip()
                == "Hủy ký Bác sĩ"
            ):
                break
        except (NoSuchElementException, StaleElementReferenceException):
            break
    time.sleep(2)

def filter_check_expand_sign_curent(driver: Driver, name: str):
    "@private"
    if filter(driver, name):
        if is_row_expandable(driver, 2):
            expand_row(driver, 2)
            for i in range(3, len(driver.find_all("tbody .ant-table-row-level-1")) + 3):
                if is_row_chuaky(driver, i):
                    _logger.info("hoan thanh or dang ky: no")
                    driver.clicking(f"tbody tr:nth-child({i})")
                    time.sleep(1)
                    sign_current(driver)
                else:
                    _logger.info("hoan thanh: yes")
        else:
            if is_row_chuaky(driver, 2):
                _logger.info("hoan thanh or dang ky: no")
                driver.clicking("tbody tr:nth-child(2)")
                sign_current(driver)
            else:
                _logger.info("hoan thanh: yes")
    time.sleep(3)

def filter_check_expand_sign_new_tab(driver: Driver, name: str, sign_fn: DriverFn):
    "@private"
    if filter(driver, name):
        if is_row_expandable(driver, 2):
            expand_row(driver, 2)
            for i in range(3, len(driver.find_all("tbody .ant-table-row-level-1")) + 3):
                if is_row_chuaky(driver, i):
                    _logger.info("hoan thanh or dang ky: no")
                    driver.clicking(f"tbody tr:nth-child({i})")
                    time.sleep(1)
                    sign_new_tab(driver, i, sign_fn)
                else:
                    _logger.info("hoan thanh: yes")
        else:
            if is_row_chuaky(driver, 2):
                _logger.info("hoan thanh or dang ky: no")
                sign_new_tab(driver, 2, sign_fn)
            else:
                _logger.info("hoan thanh: yes")
    time.sleep(3)

def tobiabenhannhikhoa(driver: Driver):
    "Filter and sign name: *Tờ bìa bệnh án nhi khoa*"
    filter_check_expand_sign_new_tab(
        driver,
        name="Tờ bìa bệnh án Nhi khoa",
        sign_fn=e.tobiabenhannhikhoa,
    )

def mucAbenhannhikhoa(driver: Driver):
    "Filter and sign name: *Mục A bệnh án nhi khoa*"
    filter_check_expand_sign_new_tab(
        driver, name="Mục A - Bệnh án Nhi khoa", sign_fn=e.mucAbenhannhikhoa
    )

def mucBtongketbenhan(driver: Driver):
    "Filter and sign name: *Mục B tổng kết bệnh án*"
    filter_check_expand_sign_new_tab(
        driver,
        name="Mục B - Tổng kết Bệnh án (Nội khoa, Nhi Khoa, Truyền nhiễm, Sơ sinh, Da liễu, DD-PHCN, HHTM)",
        sign_fn=e.mucBtongketbenhan,
    )

def phieuchidinhxetnghiem(driver: Driver):
    "Filter and sign name: *Phiếu chỉ định xét nghiệm*"
    filter_check_expand_sign_curent(driver, name="Phiếu chỉ định xét nghiệm")

def todieutri(driver: Driver):
    "Filter and sign name: *Tờ điều trị*"
    filter_check_expand_sign_new_tab(driver, name="Tờ điều trị", sign_fn=e.todieutri)

def phieuCT(driver: Driver):
    "Filter and sign name: *Phiếu chỉ định chụp CT*"
    filter_check_expand_sign_new_tab(
        driver, name="Phiếu chỉ định chụp cắt lớp vi tính (CT)", sign_fn=e.phieuCT
    )

def phieuMRI(driver: Driver):
    "Filter and sign name: *Phiếu chỉ định chụp MRI*"
    filter_check_expand_sign_new_tab(
        driver, name="Phiếu chỉ định chụp cộng hưởng từ (MRI)", sign_fn=e.phieuMRI_3
    )
