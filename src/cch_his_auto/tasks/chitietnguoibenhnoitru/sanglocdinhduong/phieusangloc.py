import datetime as dt
from cch_his_auto.driver import Driver

def set_date(driver: Driver, date: dt.date):
    driver.clear_input(".input-date").send_keys(date.strftime("%d/%m/%Y"))

def set_cannang(driver: Driver, value: str):
    driver.clear_input("#canNang").send_keys(value)

def set_chieucao(driver: Driver, value: str):
    driver.clear_input("#chieuCao").send_keys(value)

def save(driver: Driver):
    driver.clicking(".right button:nth-child(2)")

def back(driver: Driver):
    driver.clicking(".footer-btn .left button")

def save_new_phieusangloc(driver: Driver, date: dt.date, cannang: str, chieucao: str):
    set_date(driver, date)
    set_cannang(driver, cannang)
    set_chieucao(driver, chieucao)
    save(driver)
    back(driver)
