"""
### Tasks: sign patient name in editor pages
"""

import logging
import time

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains

from cch_his_auto.driver import Driver
from cch_his_auto.helper import EndOfLoop

_logger = logging.getLogger().getChild("editor")


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
    _logger.info("++++ doing phieuthuchienylenh_bn, may take a while")
    driver.waiting(".table-tbody")
    time.sleep(3)
    for col in map(lambda x: x[0], filter(lambda x: x[1], zip([3, 4, 5, 6, 7], arr))):
        try:
            _logger.debug(f"cheking row 4 col {col - 2}")
            for i in range(120):
                try:
                    _logger.debug(f"finding row 4 col {col - 2} button {i}...")
                    ele = driver.find(
                        f"table tbody tr:nth-last-child(1) td:nth-child({col}) button",
                    )
                except NoSuchElementException:
                    _logger.debug(f"-> can't find row 4 col {col - 2} button")
                    try:
                        _logger.debug(
                            f"finding row 4 col {col - 2} signature image {i}..."
                        )
                        driver.find(
                            f"table tbody tr:nth-last-child(1) td:nth-child({col}) img",
                        )
                        _logger.debug(f"-> found row 4 col {col - 2} signature image")
                        break
                    except NoSuchElementException:
                        _logger.debug(
                            f"-> can't find row 4 col {col - 2} signature image"
                        )
                        continue
                else:
                    _logger.debug(
                        f"-> found row 4 col {col - 2} button -> proceed to click"
                    )
                    ActionChains(driver).scroll_to_element(ele).pause(1).click(
                        ele
                    ).perform()
                    sign_canvas(driver, signature)
                    try:
                        driver.waiting(
                            f"table tbody tr:nth-last-child(1) td:nth-child({col}) img",
                            f"row 4 col {col - 2} signature",
                        )
                        _logger.debug(f"-> finish row 4 col {col - 2}")
                    except TimeoutException:
                        _logger.warning(
                            "get TimeoutException -> maybe clicked but didn't load"
                        )
                    finally:
                        break
            else:
                raise EndOfLoop(f"can't sign row 4 col {col - 2}")
        except Exception as e:
            _logger.warning(f"get {e} -> proceed to next in queue")
    time.sleep(2)


def phieuMRI_bn(driver: Driver, signature: str):
    "*Phiếu chỉ định MRI (bệnh nhân)*"
    _sign(
        driver,
        name="phieu mri benh nhan",
        btn_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(2) .sign-image button",
        btn_txt="Ký",
        img_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(2) .sign-image img",
        signature=signature,
    )
