from dataclasses import astuple
from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action.top_patient_info import hosobenhan
from cch_his_auto_lib.action.top_patient_info.hosobenhan import tab_hosokhamchuabenh
from .config import Config


def run(d: Driver, cfg: Config):
    c = cfg.kytenhosobenhan
    if not any(astuple(c)):
        return
    print("Start kytenhosobenhan")
    with hosobenhan.session(d):
        if c.mucAbenhannhikhoa:
            tab_hosokhamchuabenh.mucAbenhannhikhoa(d)
        if c.phieukhambenhvaovien:
            tab_hosokhamchuabenh.phieukhambenhvaovien(d)
        if c.phieusanglocdinhduong:
            tab_hosokhamchuabenh.phieusanglocdinhduong(d)
        if c.phieusoket15ngay:
            tab_hosokhamchuabenh.phieusoket15ngay(d)
        if c.phieuchidinhxetnghiem:
            tab_hosokhamchuabenh.phieuchidinhxetnghiem(d)
        if c.phieuCT:
            tab_hosokhamchuabenh.phieuCT(d)
        if c.phieuMRI:
            tab_hosokhamchuabenh.phieuMRI(d)
        if c.donthuoc:
            tab_hosokhamchuabenh.donthuoc(d)
        if c.todieutri:
            tab_hosokhamchuabenh.todieutri(d)
