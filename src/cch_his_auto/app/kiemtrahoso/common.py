from cch_his_auto.driver import Driver
from cch_his_auto.tasks.chitietnguoibenhnoitru import hosobenhan

def process(driver: Driver):
    """
    Chức năng hiện tại:
        + Tờ bìa, mục A, mục B
        + phiếu chỉ định, tờ điều trị
        + Phiếu CT, MRI
        + Phiếu giải phẫu bệnh
    """
    hosobenhan.open(driver)
    hosobenhan.tobiabenhannhikhoa(driver)
    hosobenhan.mucAbenhannhikhoa(driver)
    hosobenhan.mucBtongketbenhan(driver)
    hosobenhan.phieuchidinhxetnghiem(driver)
    hosobenhan.todieutri(driver)
    hosobenhan.phieuCT(driver)
    hosobenhan.phieuMRI(driver)
    hosobenhan.giaiphaubenh(driver)
    hosobenhan.close(driver)
