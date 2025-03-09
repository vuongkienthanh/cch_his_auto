"""
### Tasks: In giấy tờ
"""

import logging
import time
from functools import partial

from cch_his_auto import Driver
from cch_his_auto.tasks.editor import sign_name as e

_logger = logging.getLogger()

def open(driver: Driver, name: str) -> bool:
    "Click *In giấy tờ* button, then click `name`"
    driver.clicking(".footer-btn .right button:nth-child(1)", "In giấy tờ")
    _logger.info(f"======= finding link {name} ======")
    for _ in range(30):
        time.sleep(1)
        for ele in driver.find_all(".ant-dropdown-menu li a"):
            if ele.text == name:
                ele.click()
                time.sleep(3)
                return True
    else:
        _logger.warning(f"cant find {name}")
        driver.clicking(".footer-btn .right button:nth-child(1)")
        return False

def todieutri(driver: Driver):
    "`open` *Tờ điều trị*, then sign it"
    main_tab = driver.current_window_handle
    if open(driver, name="Tờ điều trị"):
        driver.goto_newtab_do_smth_then_goback(main_tab, e.todieutri)

def phieuchidinh(driver: Driver):
    "`open` *Phiếu chỉ định* , then sign it"
    if open(driver, name="Phiếu chỉ định"):
        finish = False
        for _ in range(45):
            time.sleep(1)
            _logger.info("checking finish the sign button ")
            for w in driver.find_all(".__button button"):
                if w.text == "Hủy ký Bác sĩ":
                    finish = True
                    break
            if finish:
                logging.info("phieu chi dinh already signed")
                break
            for w in driver.find_all(".__button button"):
                if w.text == "Ký Bác sĩ":
                    _logger.info("clicking the sign button ")
                    w.click()
                    time.sleep(5)
                    break
        logging.info("finish phieu chi dinh")
        logging.info("clicking close button")
        driver.find_all("button[aria-label='Close']")[1].click()
        time.sleep(3)

def phieuthuchienylenh_bs(driver: Driver, arr: tuple[bool, bool, bool, bool, bool]):
    "`open` *Phiếu thực hiện y lệnh*, then sign it (bác sĩ)"
    main_tab = driver.current_window_handle
    if open(driver, "Phiếu thực hiện y lệnh"):
        driver.goto_newtab_do_smth_then_goback(
            main_tab, partial(e.phieuthuchienylenh_bs, arr=arr)
        )

def phieuthuchienylenh_dd(driver: Driver, arr: tuple[bool, bool, bool, bool, bool]):
    "`open` *Phiếu thực hiện y lệnh*, then sign it (điều dưỡng)"
    main_tab = driver.current_window_handle
    if open(driver, "Phiếu thực hiện y lệnh"):
        driver.goto_newtab_do_smth_then_goback(
            main_tab, partial(e.phieuthuchienylenh_dd, arr=arr)
        )
