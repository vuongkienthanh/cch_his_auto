import logging
import time
from functools import partial

from cch_his_auto import Driver
from cch_his_auto.tasks import editor_sign_name as s

logger = logging.getLogger()

def pick(driver: Driver, name: str) -> bool:
    driver.clicking(".footer-btn .right button:nth-child(1)", "In giấy tờ")
    logger.info(f"======= finding link {name} ======")
    for _ in range(30):
        time.sleep(1)
        for ele in driver.find_all(".ant-dropdown-menu li a"):
            if ele.text == name:
                ele.click()
                time.sleep(3)
                return True
    else:
        logger.warning(f"cant find {name}")
        driver.clicking(".footer-btn .right button:nth-child(1)")
        return False

def todieutri(driver: Driver):
    main_tab = driver.current_window_handle
    if pick(driver, name="Tờ điều trị"):
        driver.goto_newtab_do_smth_then_goback(main_tab, s.todieutri)

def phieuchidinh(driver: Driver):
    if pick(driver, name="Phiếu chỉ định"):
        finish = False
        for _ in range(45):
            time.sleep(1)
            logger.info("checking finish the sign button ")
            for w in driver.find_all(".__button button"):
                if w.text == "Hủy ký Bác sĩ":
                    finish = True
                    break
            if finish:
                logging.info("phieu chi dinh already signed")
                break
            for w in driver.find_all(".__button button"):
                if w.text == "Ký Bác sĩ":
                    logger.info("clicking the sign button ")
                    w.click()
                    time.sleep(5)
                    break
        logging.info("finish phieu chi dinh")
        logging.info("clicking close button")
        driver.find_all("button[aria-label='Close']")[1].click()
        time.sleep(3)

def phieuthuchienylenh_bs(driver: Driver, arr: s.Row):
    main_tab = driver.current_window_handle
    if pick(driver, "Phiếu thực hiện y lệnh"):
        driver.goto_newtab_do_smth_then_goback(
            main_tab, partial(s.phieuthuchienylenh_bs, arr=arr)
        )

def phieuthuchienylenh_dd(driver: Driver, arr: s.Row):
    main_tab = driver.current_window_handle
    if pick(driver, "Phiếu thực hiện y lệnh"):
        driver.goto_newtab_do_smth_then_goback(
            main_tab, partial(s.phieuthuchienylenh_dd, arr=arr)
        )

__all__ = [
    "todieutri",
    "phieuchidinh",
    "phieuthuchienylenh_bs",
    "phieuthuchienylenh_dd",
]
