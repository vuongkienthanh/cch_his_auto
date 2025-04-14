"""
### Tasks: sign patient name in editor pages
"""

import logging
import time

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains

from cch_his_auto.driver import Driver

_logger = logging.getLogger()

def sign_canvas(driver: Driver, signature: str):
    "use when patient signature needed"
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
        "save after finish drawing signature",
    )

def _sign(
    driver: Driver, name: str, btn_css: str, btn_txt: str, img_css: str, signature: str
):
    ele = driver.waiting_to_be(btn_css, btn_txt, name)
    ele.click()
    sign_canvas(driver, signature)
    driver.waiting(img_css, "signature image")

def phieuthuchienylenh_bn(
    driver: Driver, arr: tuple[bool, bool, bool, bool, bool], signature: str
):
    "*Phiếu thực hiện y lệnh (bệnh nhân)*"
    driver.waiting(".table-tbody")
    time.sleep(3)
    for col, isok in zip([3, 4, 5, 6, 7], arr):
        if isok:
            try:
                _logger.info(f"clicking row 4 col {col - 2}")
                for _ in range(120):
                    try:
                        ele = driver.find(
                            f"table tbody tr:nth-last-child(1) td:nth-child({col}) button",
                        )
                    except NoSuchElementException:
                        try:
                            driver.find(
                                f"table tbody tr:nth-last-child(1) td:nth-child({col}) img",
                            )
                            break
                        except NoSuchElementException:
                            continue
                    else:
                        ActionChains(driver).scroll_to_element(ele).pause(1).click(
                            ele
                        ).perform()
                        sign_canvas(driver, signature)
                        try:
                            driver.waiting(
                                f"table tbody tr:nth-last-child(1) td:nth-child({col}) img",
                                f"row 4 col {col - 2} signature",
                            )
                        except TimeoutException:
                            ...
                        finally:
                            break
            except Exception as e:
                _logger.warning(e)
                continue
    _logger.info("-->>finish sign patient: phieu thuc hien y lenh bn")
    time.sleep(2)

def phieuMRI(driver: Driver, signature: str):
    "*Phiếu chỉ định MRI (bệnh nhân)*"
    _sign(
        driver,
        name="phieu mri benh nhan",
        btn_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(2) .sign-image button",
        btn_txt="Ký",
        img_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(2) .sign-image img",
        signature=signature,
    )
