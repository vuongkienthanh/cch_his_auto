"""
### Tasks: sign staff name in editor pages
"""

import logging
import time

from selenium.common import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver import ActionChains

from cch_his_auto.driver import Driver
from cch_his_auto.tasks.editor import sign_patient_name
from cch_his_auto.helper import EndOfLoop

_logger = logging.getLogger().getChild("editor")


def _sign(driver: Driver, name: str, btn_css: str, btn_txt: str, img_css: str):
    for _ in range(60):
        time.sleep(1)
        try:
            _logger.debug(f"finding {name} button")
            ele = driver.find(btn_css)
        except NoSuchElementException:
            _logger.debug("-> can't find sign button, finding signature")
            try:
                driver.find(img_css)
            except NoSuchElementException:
                _logger.debug("-> can't find signature -> continue")
                continue
            else:
                _logger.info("-> found signature already signed")
                return
        else:
            try:
                if ele.text.strip().startswith(btn_txt.strip()):
                    _logger.debug("-> found sign button with correct btn_txt")
                    ele.click()
                    driver.waiting(img_css, "signature image")
                    return
                else:
                    _logger.debug("-> found sign button but wrong btn_txt -> continue")
                    continue
            except StaleElementReferenceException as e:
                _logger.warning(f"get {e}")
                continue
    else:
        raise EndOfLoop("can't sign")


def _sign_phieuthuchienylenh(driver: Driver, row: int, col: int):
    try:
        _logger.debug(f"checking row {5 - row} col {col - 2}")
        for i in range(60):
            try:
                _logger.debug(f"finding row {5 - row} col {col - 2} button {i}...")
                ele = driver.find(
                    f"table tbody tr:nth-last-child({row}) td:nth-child({col}) button",
                )
            except NoSuchElementException:
                _logger.debug(f"-> can't find row {5 - row} col {col - 2} button")
                try:
                    _logger.debug(
                        f"finding row {5 - row} col {col - 2} signature image {i}..."
                    )
                    driver.find(
                        f"table tbody tr:nth-last-child({row}) td:nth-child({col}) img",
                    )
                    _logger.debug(f"found row {5 - row} col {col - 2} signature image")
                    break
                except NoSuchElementException:
                    _logger.debug(f"can't row {5 - row} col {col - 2} signature image")
                    continue
            else:
                _logger.debug(
                    f"-> found row {5 - row} col {col - 2} button -> proceed to click"
                )
                ActionChains(driver).scroll_to_element(ele).pause(1).click(
                    ele
                ).perform()
                try:
                    driver.waiting(
                        f"table tbody tr:nth-last-child({row}) td:nth-child({col}) img",
                        f"row {5 - row} col {col - 2} signature",
                    )
                    _logger.debug(f"-> finish row {5 - row} col {col - 2}")
                except TimeoutException:
                    _logger.warning(
                        "get TimeoutException -> maybe clicked but didn't load"
                    )
                finally:
                    break
        else:
            raise EndOfLoop(f"can't sign row {row - 5} col {col - 2}")
    except Exception as e:
        _logger.warning(f"get {e} -> proceed to next in queue")


def tobiabenhannhikhoa(driver: Driver):
    "*Tờ bìa bệnh án nhi khoa*"
    _sign(
        driver,
        name="to bia benh an nhi khoa",
        btn_css=".layout-line-item div:nth-child(2) .sign-image button",
        btn_txt="Xác nhận ký Trưởng khoa",
        img_css=".layout-line-item div:nth-child(2) .sign-image img",
    )


def mucAbenhannhikhoa(driver: Driver):
    "*Mục A bệnh án nhi khoa*"
    _sign(
        driver,
        name="muc A",
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký Bác sĩ làm bệnh án",
        img_css=".sign-image img",
    )


def mucBtongketbenhan(driver: Driver):
    "*Mục B tổng kết bệnh án*"
    _sign(
        driver,
        name="muc B",
        btn_css="td:nth-child(3) .sign-image button",
        btn_txt="Xác nhận ký Bác sĩ điều trị",
        img_css="td:nth-child(3) .sign-image img",
    )


def todieutri(driver: Driver):
    "*Tờ điều trị*"
    _sign(
        driver,
        name="to dieu tri",
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký Bác sĩ điều trị",
        img_css=".sign-image img",
    )


def phieuthuchienylenh_bs(driver: Driver, arr: tuple[bool, bool, bool, bool, bool]):
    "*Phiếu thực hiện y lệnh (bác sĩ)*"
    _logger.info("++++ doing phieuthuchienylenh_bs, may take a while")
    driver.waiting(".table-tbody")
    time.sleep(3)
    for row, col in (
        (row, col)
        for col in map(
            lambda x: x[0], filter(lambda x: x[1], zip([3, 4, 5, 6, 7], arr))
        )
        for row in [4, 3]
    ):
        _sign_phieuthuchienylenh(driver, row, col)
    time.sleep(2)


def phieuthuchienylenh_dd(driver: Driver, arr: tuple[bool, bool, bool, bool, bool]):
    "*Phiếu thực hiện y lệnh (điều dưỡng)*"
    _logger.info("++++ doing phieuthuchienylenh_dd, may take a while")
    driver.waiting(".table-tbody")
    time.sleep(3)
    for col in map(lambda x: x[0], filter(lambda x: x[1], zip([3, 4, 5, 6, 7], arr))):
        _sign_phieuthuchienylenh(driver, 2, col)
    time.sleep(2)


def phieuCT(driver: Driver):
    "*Phiếu chỉ định CT*"
    _sign(
        driver,
        name="phieu CT",
        btn_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(13) .sign-image button",
        btn_txt="Xác nhận ký Bác sĩ điều trị",
        img_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(13) .sign-image img",
    )


def phieuMRI_bschidinh(driver: Driver):
    "*Phiếu chỉ định MRI, bs chỉ định*"
    _sign(
        driver,
        name="phieu MRI bs chi dinh",
        btn_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(22) .sign-image button",
        btn_txt="Xác nhận ký Bác sĩ chỉ định",
        img_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(22) .sign-image img",
    )


def phieuMRI_bsthuchien(driver: Driver):
    "*Phiếu chỉ định MRI, bs thực hiện*"
    _sign(
        driver,
        name="phieu MRI bs thuc hien",
        btn_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(1) .sign-image button",
        btn_txt="Xác nhận ký Bác sĩ thực hiện",
        img_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(1) .sign-image img",
    )


def phieuMRI_all(driver: Driver, signature: str | None):
    "*Phiếu chỉ định MRI all*"
    phieuMRI_bschidinh(driver)
    phieuMRI_bsthuchien(driver)
    if signature:
        sign_patient_name.phieuMRI_bn(driver, signature)


def giaiphaubenh(driver: Driver):
    "*Phiếu xét nghiệm giải phẫu bệnh sinh thiết*"
    _sign(
        driver,
        name="phieu giai phau benh",
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký BÁC SĨ ĐIỀU TRỊ",
        img_css=".sign-image img",
    )
