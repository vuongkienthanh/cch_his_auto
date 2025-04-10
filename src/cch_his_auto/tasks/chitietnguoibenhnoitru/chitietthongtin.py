"""
### Tasks that operate on *Chi tiết thông tin*
###### inside "*Chi tiết người bệnh nội trú*
"""

import time

from cch_his_auto.driver import Driver

def open_dialog(driver: Driver):
    driver.clicking(
        ".thong-tin-benh-nhan .bunch-icon div:first-child",
        "xem chi tiet thong tin",
    )
    driver.waiting(".avatar__image")
    time.sleep(2)

def close_dialog(driver: Driver):
    driver.clicking(
        ".ant-modal-close:has(~.ant-modal-body .avatar__image)",
        "close chi tiet thong tin",
    )
    time.sleep(2)

def get_chieucao(driver: Driver) -> str | None:
    for _ in range(10):
        try:
            return driver.find(
                ".ant-modal:has( .avatar__image) div:nth-child(5) .ant-row div:nth-child(5) input"
            ).get_attribute("value")
        except:
            ...
    else:
        return None

def get_cannang(driver: Driver) -> str | None:
    for _ in range(10):
        try:
            return driver.find(
                ".ant-modal:has( .avatar__image) div:nth-child(5) .ant-row div:nth-child(6) input"
            ).get_attribute("value")
        except:
            ...
    else:
        return None
