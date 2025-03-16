from cch_his_auto.driver import Driver
from cch_his_auto.tasks.chitietnguoibenhnoitru import hosobenhan

APP_DETAIL = """
Chức năng hiện tại:
    + Tờ bìa, mục A, mục B
    + phiếu chỉ định, tờ điều trị
"""

def process(driver: Driver):
    hosobenhan.open(driver)
    hosobenhan.tobiabenhannhikhoa(driver)
    hosobenhan.mucAbenhannhikhoa(driver)
    hosobenhan.mucBtongketbenhan(driver)
    hosobenhan.phieuchidinhxetnghiem(driver)
    hosobenhan.todieutri(driver)
    hosobenhan.close(driver)
