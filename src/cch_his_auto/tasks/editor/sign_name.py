"""
### Tasks: sign name in editor pages
"""

import logging
import time

from cch_his_auto.driver import Driver

_logger = logging.getLogger()

def sign(driver: Driver, name: str, btn_css: str, btn_txt: str, img_css: str):
    "@private"
    driver.waiting(btn_css)
    for _ in range(100):
        time.sleep(1)
        if driver.find(btn_css).text.strip() == btn_txt:
            time.sleep(5)
            break
    else:
        return
    driver.clicking(btn_css)
    driver.waiting(img_css)
    _logger.info(f"finish sign page return image: {name}")
    time.sleep(2)

def tobiabenhannhikhoa(driver: Driver):
    "*Tờ bìa bệnh án nhi khoa*"
    sign(
        driver,
        name="to bia benh an nhi khoa",
        btn_css=".layout-line-item div:nth-child(2) .sign-image",
        btn_txt="Xác nhận ký Trưởng khoa",
        img_css=".layout-line-item div:nth-child(2) .sign-image img",
    )

def mucAbenhannhikhoa(driver: Driver):
    "*Mục A bệnh án nhi khoa*"
    sign(
        driver,
        name="muc A",
        btn_css=".sign-image",
        btn_txt="Xác nhận ký Bác sĩ làm bệnh án",
        img_css=".sign-image img",
    )

def mucBtongketbenhan(driver: Driver):
    "*Mục B tổng kết bệnh án*"
    sign(
        driver,
        name="muc B",
        btn_css="td:nth-child(3) .sign-image",
        btn_txt="Xác nhận ký Bác sĩ điều trị",
        img_css="td:nth-child(3) .sign-image img",
    )

def todieutri(driver: Driver):
    "*Tờ điều trị*"
    sign(
        driver,
        name="to dieu tri",
        btn_css=".sign-image",
        btn_txt="Xác nhận ký Bác sĩ điều trị",
        img_css=".sign-image img",
    )

def phieuthuchienylenh_bs(driver: Driver, arr: tuple[bool, bool, bool, bool, bool]):
    "*Phiếu thực hiện y lệnh (bác sĩ)*"
    driver.waiting(".table-tbody")
    time.sleep(5)
    for col, isok in zip([3, 4, 5, 6, 7], arr):
        if isok:
            for row in [4, 3]:
                try:
                    driver.clicking(
                        f"table tbody tr:nth-last-child({row}) td:nth-child({col}) button",
                        f"row {row} col {col}",
                    )
                    driver.waiting(
                        f"table tbody tr:nth-last-child({row}) td:nth-child({col}) img",
                        f"row {row} col {col}",
                    )
                except Exception as e:
                    _logger.warning(e)
                    continue
    _logger.info("finish sign page: phieu thuc hien y lenh bs")
    time.sleep(2)

def phieuthuchienylenh_dd(driver: Driver, arr: tuple[bool, bool, bool, bool, bool]):
    "*Phiếu thực hiện y lệnh (điều dưỡng)*"
    driver.waiting(".table-tbody")
    time.sleep(5)
    for col, isok in zip([3, 4, 5, 6, 7], arr):
        if isok:
            try:
                driver.clicking(
                    f"table tbody tr:nth-last-child(2) td:nth-child({col}) button",
                    f"row 2 col {col}",
                )
                driver.waiting(
                    f"table tbody tr:nth-last-child(2) td:nth-child({col}) img",
                    f"row 2 col {col}",
                )
            except Exception as e:
                _logger.warning(e)
                continue
    _logger.info("finish sign page: phieu thuc hien y lenh dd")
    time.sleep(2)
