from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action.chitietnguoibenhnoitru import (
    thongtinchung,
    change_tab,
)
from cch_his_auto_lib.action.top_info import hosobenhan
from cch_his_auto_lib.action.top_info.hosobenhan import tab_dvkt
from cch_his_auto_lib.action.chitietnguoibenhnoitru.tabs.thongtinchung import (
    thongtinvaovien_dialog,
)
from .config import Config


def run(d: Driver, cfg: Config):
    if not cfg.nhommau:
        return
    print("Start nhommau")
    change_tab(d, thongtinchung.TAB_NUMBER)
    bloodtype = thongtinchung.get_bloodtype(d)
    if bloodtype is None:
        with hosobenhan.dialog(d, tab_dvkt.TAB_NUMBER):
            found_bloodtype = tab_dvkt.get_bloodtype(d)
        if found_bloodtype is not None:
            with thongtinvaovien_dialog.session(d):
                thongtinvaovien_dialog.set_bloodtype(d, found_bloodtype)
