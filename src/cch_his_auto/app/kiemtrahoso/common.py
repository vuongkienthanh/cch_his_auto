from cch_his_auto.driver import Driver
from cch_his_auto.tasks.chitietnguoibenhnoitru import hosobenhan, danhsachnguoibenh
from cch_his_auto.tasks import danhsachnguoibenhnoitru

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

def first_patient(driver: Driver, ma_hs: int):
    danhsachnguoibenhnoitru.goto_patient(driver, ma_hs)

def next_patient(driver: Driver, ma_hs: int):
    danhsachnguoibenh.open(driver)
    danhsachnguoibenh.goto_patient(driver, ma_hs)
