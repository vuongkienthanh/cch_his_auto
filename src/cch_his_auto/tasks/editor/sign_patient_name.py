"""
### Tasks: sign patient in editor pages
"""

import logging
import time

from cch_his_auto.driver import Driver

_logger = logging.getLogger()

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
                time.sleep(5)
                driver.clicking("canvas")
                driver.clicking(
                    ".ant-modal .bottom-action-right button",
                    "save after finish drawing",
                )
                driver.waiting(
                    f"table tbody tr:nth-last-child(1) td:nth-child({col}) img",
                    f"row 1 col {col}",
                )
            except Exception as e:
                _logger.warning(e)
                continue
    _logger.info("finish sign patient: phieu thuc hien y lenh")
    time.sleep(2)
