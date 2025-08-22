from tkinter import messagebox

from cch_his_auto.app import PROFILE_PATH

from cch_his_auto.global_db import create_connection
from cch_his_auto.common_ui.button_frame import RunConfig
from cch_his_auto.common_tasks.navigation import first_patient, next_patient

from cch_his_auto_lib.driver import start_driver
from cch_his_auto_lib.tasks import auth, danhsachnguoibenhnoitru
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import tab_thongtinchung
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.tab_thongtinchung import (
    edit_thongtinravien,
)

from . import config


def run(cfg: config.Config, run_cfg: RunConfig):
    if not config.is_valid(cfg):
        messagebox.showerror(message="chưa đủ thông tin")
        return

    machanthuong_kemtheo_missing = []
    discharge_date_is_none = []
    appointment_date_is_sat_sun = []

    viettat_dict = {
        "hp": "hậu phẫu",
        "pt": "phẫu thuật",
        "nmc": "ngoài màng cứng",
        "dmc": "dưới màng cứng",
    }

    def check_machanthuong_kemtheo(ma_hs: int):
        diagnosis = tab_thongtinchung.get_discharge_diagnosis(d)
        if diagnosis is not None:
            if diagnosis.startswith("S") and not any(
                [d[0] in "WYV" for d in tab_thongtinchung.get_discharge_comorbid(d)]
            ):
                machanthuong_kemtheo_missing.append(ma_hs)

    def check_discharge_date(ma_hs: int):
        date = tab_thongtinchung.get_discharge_date(d)
        if date is None:
            discharge_date_is_none.append(ma_hs)

    with start_driver(headless=run_cfg["headless"], profile_path=PROFILE_PATH) as d:

        def check_appointment_date(ma_hs: int):
            date = tab_thongtinchung.get_appointment_date(d)
            # is saturday / sunday
            if date is not None:
                if date.weekday() in [5, 6]:
                    appointment_date_is_sat_sun.append(ma_hs)

        def sua_viet_tat():
            # mở rộng chữ viết tắt
            detail = tab_thongtinchung.get_discharge_diagnosis_detail(d)
            if detail is not None:
                detail = detail.lower()
                for k, v in viettat_dict.items():
                    detail = detail.replace(k, v)
                with edit_thongtinravien.session(d):
                    edit_thongtinravien.set_discharge_diagnosis_detail(d, detail)
            treatment = tab_thongtinchung.get_treatment(d)
            if treatment is not None:
                treatment = treatment.lower()
                for k, v in viettat_dict.items():
                    treatment = treatment.replace(k, v)
                with edit_thongtinravien.session(d):
                    edit_thongtinravien.set_treatment(d, treatment)

        def check(ma_hs: int):
            check_machanthuong_kemtheo(ma_hs)
            check_discharge_date(ma_hs)
            check_appointment_date(ma_hs)
            sua_viet_tat()

        with auth.session(d, cfg["username"], cfg["password"], cfg["department"]):
            with create_connection() as con:
                danhsachnguoibenhnoitru.filter_trangthainguoibenh_check_all(d)

                ma_hs = cfg["listing"].pop()
                first_patient(d, con, ma_hs)
                check(ma_hs)

                while len(cfg["listing"]) > 0:
                    ma_hs = cfg["listing"].pop()
                    next_patient(d, con, ma_hs)
                    check(ma_hs)

    if len(machanthuong_kemtheo_missing) > 0:
        messagebox.showwarning(
            message="Thiếu mã chấn thương kèm theo:\n"
            + "\n".join([str(x) for x in machanthuong_kemtheo_missing])
        )
    if len(discharge_date_is_none) > 0:
        messagebox.showwarning(
            message="Thiếu ngày ra viện:\n"
            + "\n".join([str(x) for x in discharge_date_is_none])
        )
    if len(appointment_date_is_sat_sun) > 0:
        messagebox.showwarning(
            message="Ngày tái khám T7 CN:\n"
            + "\n".join([str(x) for x in appointment_date_is_sat_sun])
        )
    messagebox.showinfo(message="finish")
