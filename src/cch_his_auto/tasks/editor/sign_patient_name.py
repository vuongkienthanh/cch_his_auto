"""
### Tasks: sign patient in editor pages
"""

import logging
import time

from selenium.common import NoSuchElementException

from cch_his_auto.driver import Driver

_logger = logging.getLogger()

def sign_patient(driver: Driver, signature:str):
    driver.waiting("canvas")
    script = """
        let c = document.querySelector('canvas');
        let ctx = c.getContext('2d');
        let image = new Image();
        image.onload = function() {{
            ctx.drawImage(image, 0, 0, 400, 200);
        }};
        image.src = '{signature}'
        """.format(signature=signature)

    driver.execute_script(script)
    time.sleep(3)
    driver.clicking("canvas")
    driver.clicking(
        ".ant-modal .bottom-action-right button",
        "save after finish drawing",
    )

def phieuthuchienylenh(
    driver: Driver, arr: tuple[bool, bool, bool, bool, bool], signature: str
):
    "*Phiếu thực hiện y lệnh (bệnh nhân)*"
    driver.waiting(".table-tbody")
    time.sleep(5)
    for col, isok in zip([3, 4, 5, 6, 7], arr):
        if isok:
            try:
                driver.clicking(
                    f"table tbody tr:nth-last-child(1) td:nth-child({col}) button",
                    f"row 1 col {col}",
                )
                sign_patient(driver, signature)
                driver.waiting(
                    f"table tbody tr:nth-last-child(1) td:nth-child({col}) img",
                    f"row 1 col {col}",
                )
            except Exception as e:
                _logger.warning(e)
                continue
    _logger.info("finish sign patient: phieu thuc hien y lenh")
    time.sleep(2)

def phieuMRI(driver: Driver, signature: str):
    "*Phiếu chỉ định MRI, bệnh nhân*"
    btn_css = ".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(2) .sign-image button"
    img_css = ".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(2) .sign-image img"
    try:
        driver.waiting(btn_css)
    except NoSuchElementException:
        return
    for _ in range(20):
        time.sleep(1)
        try:
            if driver.find(btn_css).text.strip() == "Ký":
                break
        except:
            ...
    else:
        return
    driver.clicking(btn_css)
    sign_patient(driver, signature)
    driver.waiting(img_css)
    _logger.info("finish sign page return image: phieu mri benh nhan")
    time.sleep(2)
