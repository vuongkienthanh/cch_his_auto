from cch_his_auto.driver import Driver
from cch_his_auto.tasks.chitietnguoibenhnoitru import hosobenhan

def process(driver: Driver):
    hosobenhan.open(driver)
    hosobenhan.tobiabenhannhikhoa(driver)
    hosobenhan.mucAbenhannhikhoa(driver)
    hosobenhan.mucBtongketbenhan(driver)
    hosobenhan.phieuchidinhxetnghiem(driver)
    hosobenhan.todieutri(driver)
    hosobenhan.close(driver)
