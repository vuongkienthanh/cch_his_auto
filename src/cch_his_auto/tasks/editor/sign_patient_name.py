"""
### Tasks: sign patient in editor pages
"""

import logging
import time

from selenium.common import NoSuchElementException
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
        "save after finish drawing",
    )

def sign(
    driver: Driver, name: str, btn_css: str, btn_txt: str, img_css: str, signature: str
):
    "@private"
    try:
        driver.waiting(btn_css)
    except NoSuchElementException:
        return
    for _ in range(20):
        time.sleep(1)
        try:
            if driver.find(btn_css).text.strip() == btn_txt:
                break
        except:
            ...
    else:
        return
    driver.clicking(btn_css)
    sign_canvas(driver, signature)
    driver.waiting(img_css)
    _logger.info(f"finish sign page return image: {name}")

def phieuthuchienylenh(
    driver: Driver, arr: tuple[bool, bool, bool, bool, bool], signature: str
):
    "*Phiếu thực hiện y lệnh (bệnh nhân)*"
    driver.waiting(".table-tbody")
    time.sleep(5)
    for col, isok in zip([3, 4, 5, 6, 7], arr):
        if isok:
            try:
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
                        except:
                            continue
                    ActionChains(driver).scroll_to_element(ele).pause(1).click(
                        ele
                    ).perform()
                    sign_canvas(driver, signature)
                    driver.waiting(
                        f"table tbody tr:nth-last-child(1) td:nth-child({col}) img",
                        f"-->>done clicking row 4 col {col - 2} ",
                    )
                    break
                # driver.clicking(
                #     f"table tbody tr:nth-last-child(1) td:nth-child({col}) button",
                #     f"row 4 col {col}",
                # )
                # sign_canvas(driver, signature)
                # driver.waiting(
                #     f"table tbody tr:nth-last-child(1) td:nth-child({col}) img",
                #     f"-->>done row 4 col {col}",
                # )
            except Exception as e:
                _logger.warning(e)
                continue
    _logger.info("-->>finish sign patient: phieu thuc hien y lenh bn")
    time.sleep(2)

def phieuMRI(driver: Driver, signature: str):
    "*Phiếu chỉ định MRI (bệnh nhân)*"
    sign(
        driver,
        name="phieu mri benh nhan",
        btn_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(2) .sign-image button",
        btn_txt="Ký",
        img_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(2) .sign-image img",
        signature=signature,
    )
