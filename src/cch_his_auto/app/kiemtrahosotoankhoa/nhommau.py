from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action.chitietnguoibenhnoitru.tabs import (
    thongtinchung,
    change_tab,
)
from cch_his_auto_lib.action.top_patient_info import hosobenhan
from cch_his_auto_lib.action.top_patient_info.hosobenhan import tab_dvkt
from cch_his_auto_lib.action.chitietnguoibenhnoitru.tabs.thongtinchung import (
    edit_thongtinvaovien,
)


def run(d: Driver):
    change_tab(d, thongtinchung.TAB_NUMBER)
    bloodtype = thongtinchung.get_bloodtype(d)
    if bloodtype is None:
        with hosobenhan.session(d, tab_dvkt.TAB_NUMBER):
            found_bloodtype = tab_dvkt.get_bloodtype(d)
        if found_bloodtype is not None:
            with edit_thongtinvaovien.session(d):
                edit_thongtinvaovien.set_bloodtype(d, found_bloodtype)
