"""
### Tasks: sign staff name in editor pages
"""

import logging
import time

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains

from cch_his_auto.driver import Driver
from cch_his_auto.tasks.editor import sign_patient_name

_logger = logging.getLogger().getChild("editors")

def _sign(driver: Driver, name: str, btn_css: str, btn_txt: str, img_css: str):
    ele = driver.waiting_to_be(btn_css, btn_txt, name)
    _logger.debug("click sign button")
    ele.click()
    driver.waiting(img_css, "signature image")

def tobiabenhannhikhoa(driver: Driver):
    "*Tờ bìa bệnh án nhi khoa*"
    _sign(
        driver,
        name="to bia benh an nhi khoa",
        btn_css=".layout-line-item div:nth-child(2) .sign-image button",
        btn_txt="Xác nhận ký Trưởng khoa",
        img_css=".layout-line-item div:nth-child(2) .sign-image img",
    )
    _logger.debug("-> finish sign editor: tờ bìa bệnh án nhi khoa")

def mucAbenhannhikhoa(driver: Driver):
    "*Mục A bệnh án nhi khoa*"
    _sign(
        driver,
        name="muc A",
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký Bác sĩ làm bệnh án",
        img_css=".sign-image img",
    )
    _logger.debug("-> finish sign editor: mục A")

def mucBtongketbenhan(driver: Driver):
    "*Mục B tổng kết bệnh án*"
    _sign(
        driver,
        name="muc B",
        btn_css="td:nth-child(3) .sign-image button",
        btn_txt="Xác nhận ký Bác sĩ điều trị",
        img_css="td:nth-child(3) .sign-image img",
    )
    _logger.debug("-> finish sign editor: mục B")

def todieutri(driver: Driver):
    "*Tờ điều trị*"
    _sign(
        driver,
        name="to dieu tri",
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký Bác sĩ điều trị",
        img_css=".sign-image img",
    )
    _logger.debug("-> finish sign editor: tờ điều trị")

def phieuthuchienylenh_bs(driver: Driver, arr: tuple[bool, bool, bool, bool, bool]):
    "*Phiếu thực hiện y lệnh (bác sĩ)*"
    driver.waiting(".table-tbody")
    time.sleep(3)
    for col, isok in zip([3, 4, 5, 6, 7], arr):
        if isok:
            for row in [4, 3]:
                try:
                    _logger.debug(f"checking row {5 - row} col {col - 2}")
                    for i in range(120):
                        try:
                            _logger.debug(
                                f"finding row {5 - row} col {col - 2} button {i}..."
                            )
                            ele = driver.find(
                                f"table tbody tr:nth-last-child({row}) td:nth-child({col}) button",
                            )
                        except NoSuchElementException:
                            _logger.debug(
                                f"-> can't find row {5 - row} col {col - 2} button"
                            )
                            try:
                                _logger.debug(
                                    f"finding row {5 - row} col {col - 2} signature image {i}..."
                                )
                                driver.find(
                                    f"table tbody tr:nth-last-child({row}) td:nth-child({col}) img",
                                )
                                _logger.debug(
                                    f"found row {5 - row} col {col - 2} signature image"
                                )
                                break
                            except NoSuchElementException:
                                _logger.debug(
                                    f"can't row {5 - row} col {col - 2} signature image"
                                )
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
                        raise Exception("end of loop")
                except Exception as e:
                    _logger.warning(
                        f"get {e} -> can't sign name on this cell -> proceed to next in queue"
                    )
    _logger.debug("-> finish sign editor: phiếu thực hiện y lệnh bs")
    time.sleep(2)

def phieuthuchienylenh_dd(driver: Driver, arr: tuple[bool, bool, bool, bool, bool]):
    "*Phiếu thực hiện y lệnh (điều dưỡng)*"
    driver.waiting(".table-tbody")
    time.sleep(3)
    for col, isok in zip([3, 4, 5, 6, 7], arr):
        if isok:
            try:
                _logger.debug(f"checking row 3 col {col - 2}")
                for i in range(120):
                    try:
                        _logger.debug(f"finding row 3 col {col - 2} button {i}...")
                        ele = driver.find(
                            f"table tbody tr:nth-last-child(2) td:nth-child({col}) button",
                        )
                    except NoSuchElementException:
                        _logger.debug(f"-> can't find row 3 col {col - 2} button")
                        try:
                            _logger.debug(
                                f"finding row 3 col {col - 2} signature image {i}..."
                            )
                            driver.find(
                                f"table tbody tr:nth-last-child(2) td:nth-child({col}) img",
                            )
                            _logger.debug(
                                f"-> found row 3 col {col - 2} signature image"
                            )
                            break
                        except NoSuchElementException:
                            _logger.debug(
                                f"-> can't find row 3 col {col - 2} signature image"
                            )
                            continue
                    else:
                        _logger.debug(
                            f"-> found row 3 col {col - 2} button -> proceed to click"
                        )
                        ActionChains(driver).scroll_to_element(ele).pause(1).click(
                            ele
                        ).perform()
                        try:
                            driver.waiting(
                                f"table tbody tr:nth-last-child(2) td:nth-child({col}) img",
                                f"row 3 col {col - 2} signature",
                            )
                            _logger.debug(f"-> finish row 3 col {col - 2}")
                        except TimeoutException:
                            _logger.warning(
                                "get TimeoutException -> maybe clicked but didn't load"
                            )
                        finally:
                            break
                else:
                    raise Exception("end of loop")
            except Exception as e:
                _logger.warning(
                    f"get {e} -> can't sign name on this cell -> proceed to next in queue"
                )
    _logger.debug("-> finish sign editor: phiếu thực hiện y lệnh dd")
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
    _logger.debug("-> finish sign editor: phiếu CT")

def phieuMRI_bschidinh(driver: Driver):
    "*Phiếu chỉ định MRI, bs chỉ định*"
    _sign(
        driver,
        name="phieu MRI bs chi dinh",
        btn_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(22) .sign-image button",
        btn_txt="Xác nhận ký Bác sĩ chỉ định",
        img_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(22) .sign-image img",
    )
    _logger.debug("-> finish sign editor: phiếu MRI bs chỉ định")

def phieuMRI_bsthuchien(driver: Driver):
    "*Phiếu chỉ định MRI, bs thực hiện*"
    _sign(
        driver,
        name="phieu MRI bs thuc hien",
        btn_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(1) .sign-image button",
        btn_txt="Xác nhận ký Bác sĩ thực hiện",
        img_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(1) .sign-image img",
    )
    _logger.debug("-> finish sign editor: phiếu MRI bs thực hiện")

def phieuMRI_all(driver: Driver, signature: str | None):
    "*Phiếu chỉ định MRI all*"
    phieuMRI_bschidinh(driver)
    phieuMRI_bsthuchien(driver)
    if signature:
        sign_patient_name.phieuMRI(driver, signature)

def giaiphaubenh(driver: Driver):
    "*Phiếu xét nghiệm giải phẫu bệnh sinh thiết*"
    _sign(
        driver,
        name="phieu giai phau benh",
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký BÁC SĨ ĐIỀU TRỊ",
        img_css=".sign-image img",
    )
    _logger.debug("-> finish sign editor: phiếu giải phẫu bệnh")
