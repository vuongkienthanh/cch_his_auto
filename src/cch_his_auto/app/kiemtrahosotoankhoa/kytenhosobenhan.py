from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action.top_patient_info import hosobenhan
from cch_his_auto_lib.action.top_patient_info.hosobenhan import tab_hosokhamchuabenh


def run(d: Driver):
    print("Start kytenhosobenhan")
    with hosobenhan.session(d):
        tab_hosokhamchuabenh.mucAbenhannhikhoa(d)
        tab_hosokhamchuabenh.phieukhambenhvaovien(d)

        tab_hosokhamchuabenh.phieusanglocdinhduong(d)
        tab_hosokhamchuabenh.phieusoket15ngay(d)

        tab_hosokhamchuabenh.phieuchidinhxetnghiem(d)
        tab_hosokhamchuabenh.phieuCT(d)
        tab_hosokhamchuabenh.phieuMRI(d)

        tab_hosokhamchuabenh.donthuoc(d)
        tab_hosokhamchuabenh.todieutri(d)
