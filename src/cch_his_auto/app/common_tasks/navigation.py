from sqlite3 import Connection

from cch_his_auto.driver import Driver
from cch_his_auto.tasks.chitietnguoibenhnoitru import danhsachnguoibenh
from cch_his_auto.tasks import danhsachnguoibenhnoitru
from cch_his_auto.app.global_db import get_url_from_db

def first_patient(driver: Driver, con: Connection, ma_hs: int):
    if url := get_url_from_db(con, ma_hs):
        driver.goto(url)
    else:
        danhsachnguoibenhnoitru.goto_patient(driver, ma_hs)

def next_patient(driver: Driver, con: Connection, ma_hs: int):
    if url := get_url_from_db(con, ma_hs):
        driver.goto(url)
    else:
        danhsachnguoibenh.open(driver)
        danhsachnguoibenh.goto_patient(driver, ma_hs)
