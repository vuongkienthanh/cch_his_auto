from dataclasses import astuple
from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action.top_info import hosobenhan
from cch_his_auto_lib.action.top_info.hosobenhan.tab_hosokhamchuabenh import (
    sign as tab_hskcb_sign,
)
from .config import Config


def run(d: Driver, cfg: Config):
    c = cfg.kytenhosobenhan
    if not any(astuple(c)):
        return
    print("Start kytenhosobenhan")
    with hosobenhan.dialog(d):
        if c.mucAbenhannhikhoa:
            tab_hskcb_sign.mucAbenhannhikhoa(d)
        if c.phieukhambenhvaovien:
            tab_hskcb_sign.phieukhambenhvaovien(d)
        if c.phieusanglocdinhduong:
            tab_hskcb_sign.phieusanglocdinhduong(d)
        if c.phieusoket15ngay:
            tab_hskcb_sign.phieusoket15ngay(d)
        if c.phieuchidinhxetnghiem:
            tab_hskcb_sign.phieuchidinhxetnghiem(d)
        if c.phieuCT:
            tab_hskcb_sign.phieuCT(d)
        if c.phieuMRI:
            tab_hskcb_sign.phieuMRI(d)
        if c.donthuoc:
            tab_hskcb_sign.donthuoc(d)
        if c.todieutri:
            tab_hskcb_sign.todieutri(d)
