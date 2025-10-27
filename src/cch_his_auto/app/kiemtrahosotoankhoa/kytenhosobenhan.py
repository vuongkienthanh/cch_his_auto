from dataclasses import astuple
from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action.top_info import hosobenhan
from cch_his_auto_lib.action.top_info.hosobenhan import tab_hosokhamchuabenh
from .config import Config


def run(d: Driver, cfg: Config):
    c = cfg.kytenhosobenhan
    if not any(astuple(c)):
        return
    print("Start kytenhosobenhan")
    with hosobenhan.dialog(d):
        if c.mucAbenhannhikhoa:
            tab_hosokhamchuabenh.sign_mucAbenhannhikhoa(d)
        if c.phieukhambenhvaovien:
            tab_hosokhamchuabenh.sign_phieukhambenhvaovien(d)
        if c.phieusanglocdinhduong:
            tab_hosokhamchuabenh.sign_phieusanglocdinhduong(d)
        if c.phieusoket15ngay:
            tab_hosokhamchuabenh.sign_phieusoket15ngay(d)
        if c.phieuchidinhxetnghiem:
            tab_hosokhamchuabenh.sign_phieuchidinhxetnghiem(d)
        if c.phieuCT:
            tab_hosokhamchuabenh.sign_phieuCT(d)
        if c.phieuMRI:
            tab_hosokhamchuabenh.sign_phieuMRI(d)
        if c.donthuoc:
            tab_hosokhamchuabenh.sign_donthuoc(d)
        if c.todieutri:
            tab_hosokhamchuabenh.sign_todieutri(d)
