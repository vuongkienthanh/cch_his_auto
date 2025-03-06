import logging
import time
from functools import partial

from cch_his_auto import Driver
from cch_his_auto.tasks import raw_page_sign_name as s

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/to-dieu-tri"
logger = logging.getLogger()

def choose_InGiayTo(driver: Driver, name: str) -> bool:
    driver.clicking(".footer-btn .right button:nth-child(1)", "In giấy tờ")
    logger.info(f"======= finding link {name} ======")
    for _ in range(30):
        time.sleep(1)
        for ele in driver.findings(".ant-dropdown-menu li a"):
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
    if choose_InGiayTo(driver, name="Tờ điều trị"):
        driver.goto_newtab_do_smth_then_goback(main_tab, s.todieutri)

def phieuchidinh(driver: Driver):
    if choose_InGiayTo(driver, name="Phiếu chỉ định"):
        finish = False
        for _ in range(45):
            time.sleep(1)
            logger.info("checking finish the sign button ")
            for w in driver.findings(".__button button"):
                if w.text == "Hủy ký Bác sĩ":
                    finish = True
                    break
            if finish:
                logging.info("phieu chi dinh already signed")
                break
            for w in driver.findings(".__button button"):
                if w.text == "Ký Bác sĩ":
                    logger.info("clicking the sign button ")
                    w.click()
                    time.sleep(5)
                    break
        logging.info("finish phieu chi dinh")
        logging.info("clicking close button")
        driver.findings("button[aria-label='Close']")[1].click()
        time.sleep(3)

def phieuthuchienylenh_bs(driver: Driver, arr: s.Row):
    main_tab = driver.current_window_handle
    if choose_InGiayTo(driver, "Phiếu thực hiện y lệnh"):
        driver.goto_newtab_do_smth_then_goback(
            main_tab, partial(s.phieuthuchienylenh_bs, arr=arr)
        )

def phieuthuchienylenh_dd(driver: Driver, arr: s.Row):
    main_tab = driver.current_window_handle
    if choose_InGiayTo(driver, "Phiếu thực hiện y lệnh"):
        driver.goto_newtab_do_smth_then_goback(
            main_tab, partial(s.phieuthuchienylenh_dd, arr=arr)
        )
