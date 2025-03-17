from cch_his_auto.driver import Driver
from cch_his_auto.tasks.chitietnguoibenhnoitru import danhsachnguoibenh
from cch_his_auto.tasks import danhsachnguoibenhnoitru

def first_patient(driver: Driver, ma_hs: int):
    danhsachnguoibenhnoitru.goto_patient(driver, ma_hs)

def next_patient(driver: Driver, ma_hs: int):
    danhsachnguoibenh.open(driver)
    danhsachnguoibenh.goto_patient(driver, ma_hs)
