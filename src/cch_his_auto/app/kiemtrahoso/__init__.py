import datetime as dt
import tkinter as tk
from tkinter import messagebox, scrolledtext

from cch_his_auto.app import PROFILE_PATH, _lgr

from cch_his_auto.global_db import create_connection
from cch_his_auto.common_ui.staff_info import UsernamePasswordDeptFrame
from cch_his_auto.common_ui.button_frame import ButtonFrame, RunConfig, setLogLevel
from cch_his_auto.common_tasks.navigation import first_patient, next_patient
from cch_his_auto.common_tasks.signature import try_get_signature

from . import config

from cch_his_auto_lib.driver import start_global_driver
from cch_his_auto_lib.tasks import auth, danhsachnguoibenhnoitru
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.tab_thongtinchung import (
    edit_thongtinvaovien,
    edit_thongtinravien,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import (
    tab_thongtinchung,
    top_chitietthongtin,
    top_hosobenhan,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.top_hosobenhan import (
    tab_mau,
    tab_hosokhamchuabenh,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.bot_sanglocdinhduong import (
    add_all_phieusanglocdinhduong,
)


TITLE = "Kiểm tra hồ sơ"


class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        info = tk.LabelFrame(self, text="Thông tin đăng nhập")
        bacsi = UsernamePasswordDeptFrame(info, text="Bác sĩ ký tên")
        bacsi.grid(row=0, column=0)
        info.grid(row=0, column=0, sticky="N", pady=20)

        mainframe = tk.Frame(self)
        mainframe.grid(row=1, column=0, sticky="NSEW")
        discharged_var = tk.BooleanVar()
        is_finalday_var = tk.BooleanVar()
        tk.Checkbutton(mainframe, text="đã xuất viện", variable=discharged_var).grid(
            row=0, column=0, padx=20, pady=20, sticky="W"
        )
        tk.Checkbutton(mainframe, text="ngày cuối cùng", variable=is_finalday_var).grid(
            row=0, column=1, padx=20, pady=20, sticky="W"
        )
        tk.Label(mainframe, text="Danh sách mã hồ sơ:", anchor="w").grid(
            row=1, column=0, padx=20, sticky="NEW", columnspan=2
        )
        listing = scrolledtext.ScrolledText(mainframe)
        listing.grid(row=2, column=0, padx=20, sticky="NSEW", columnspan=2)

        button_frame = ButtonFrame(self)
        button_frame.grid(row=0, column=1, rowspan=2, padx=20, sticky="S", pady=(0, 20))

        def load():
            cfg = config.load()

            bacsi.set_username(cfg["username"])
            bacsi.set_password(cfg["password"])
            bacsi.set_department(cfg["department"])

            listing.delete("1.0", "end")
            listing.insert("1.0", cfg["listing"])
            discharged_var.set(cfg["discharged"])
            is_finalday_var.set(cfg["is_final_day"])

            button_frame.load_config()

        def get_config() -> config.Config:
            return {
                "username": bacsi.get_username(),
                "password": bacsi.get_password(),
                "department": bacsi.get_department(),
                "listing": listing.get("1.0", "end"),
                "discharged": discharged_var.get(),
                "is_final_day": is_finalday_var.get(),
            }

        def save():
            if messagebox.askyesno(message="Save?"):
                config.save(get_config())
                button_frame.save_config()
                messagebox.showinfo(message="Đã lưu")

        button_frame.bind_load(load)
        button_frame.bind_save(save)
        button_frame.bind_run(lambda: run(get_config(), button_frame.get_config()))


def run(cfg: config.Config, run_cfg: RunConfig):
    if not config.is_valid(cfg):
        messagebox.showerror(message="chưa đủ thông tin")
        return

    setLogLevel(run_cfg)
    listing = [int(ma_hs) for ma_hs in cfg["listing"].strip().splitlines()]
    with start_global_driver(
        headless=run_cfg["headless"], profile_path=PROFILE_PATH
    ) as driver:
        with auth.session(cfg["username"], cfg["password"], cfg["department"]):
            if cfg["is_final_day"]:
                if not pre_run_final_day_check(listing):
                    return
                driver.goto(danhsachnguoibenhnoitru.URL)
                process = process_final_day
            else:
                process = process_normal_day
            with create_connection() as con:
                if cfg["discharged"]:
                    danhsachnguoibenhnoitru.filter_trangthainguoibenh([10])

                ma_hs = listing.pop()
                first_patient(con, ma_hs)
                signature = try_get_signature(con, ma_hs)
                process(signature)

                while len(listing) > 0:
                    ma_hs = listing.pop()
                    next_patient(con, ma_hs)
                    signature = try_get_signature(con, ma_hs)
                    process(signature)

    messagebox.showinfo(message="finish")


def process_normal_day(signature: str | None):
    admission_date = tab_thongtinchung.get_admission_date()
    add_all_phieusanglocdinhduong(admission_date)

    # điền thông tin nhóm máu
    bloodtype = tab_thongtinchung.get_bloodtype()
    if bloodtype is None:
        with top_hosobenhan.session(tab_mau.TAB_NUMBER):
            found_bloodtype = tab_mau.get_bloodtype()
        if found_bloodtype is not None:
            with edit_thongtinvaovien.session():
                edit_thongtinvaovien.set_bloodtype(found_bloodtype)

    with top_hosobenhan.session():
        tab_hosokhamchuabenh.phieuchidinhxetnghiem()
        tab_hosokhamchuabenh.todieutri(dt.date.today())
        tab_hosokhamchuabenh.phieuCT(signature)
        tab_hosokhamchuabenh.phieuMRI(signature)
        tab_hosokhamchuabenh.giaiphaubenh()
        tab_hosokhamchuabenh.phieusanglocdinhduong()
        tab_hosokhamchuabenh.phieuchidinhPTTT()
        tab_hosokhamchuabenh.phieusoket15ngay()
        tab_hosokhamchuabenh.phieucamkettruyenmau(signature)
        # tab_hosokhamchuabenh.phieucamkettta5( signature) # HIS BUG


def process_final_day(signature: str | None):
    admission_date = tab_thongtinchung.get_admission_date()
    add_all_phieusanglocdinhduong(admission_date)
    discharge_date = tab_thongtinchung.get_discharge_date()

    # mở rộng chữ viết tắt
    viettat_dict = {
        "hp": "hậu phẫu",
        "pt": "phẫu thuật",
        "nmc": "ngoài màng cứng",
        "dmc": "dưới màng cứng",
    }
    detail = tab_thongtinchung.get_discharge_diagnosis_detail()
    if detail is not None:
        detail = detail.lower()
        for k, v in viettat_dict.items():
            detail = detail.replace(k, v)
        with edit_thongtinravien.session():
            edit_thongtinravien.set_discharge_diagnosis_detail(detail)
    treatment = tab_thongtinchung.get_treatment()
    if treatment is not None:
        treatment = treatment.lower()
        for k, v in viettat_dict.items():
            treatment = treatment.replace(k, v)
        with edit_thongtinravien.session():
            edit_thongtinravien.set_treatment(treatment)

    # điền thông tin nhóm máu
    bloodtype = tab_thongtinchung.get_bloodtype()
    if bloodtype is None:
        with top_hosobenhan.session(tab_mau.TAB_NUMBER):
            found_bloodtype = tab_mau.get_bloodtype()
        if found_bloodtype is not None:
            with edit_thongtinvaovien.session():
                edit_thongtinvaovien.set_bloodtype(found_bloodtype)

    with top_hosobenhan.session():
        # tab_hosokhamchuabenh.tobiabenhannhikhoa()
        tab_hosokhamchuabenh.mucAbenhannhikhoa()
        tab_hosokhamchuabenh.mucBtongketbenhan()
        tab_hosokhamchuabenh.phieukhambenhvaovien()
        tab_hosokhamchuabenh.phieuchidinhxetnghiem()
        tab_hosokhamchuabenh.todieutri(discharge_date)
        tab_hosokhamchuabenh.phieuCT(signature)
        tab_hosokhamchuabenh.phieuMRI(signature)
        tab_hosokhamchuabenh.giaiphaubenh()
        tab_hosokhamchuabenh.phieusanglocdinhduong()
        tab_hosokhamchuabenh.phieuchidinhPTTT()
        tab_hosokhamchuabenh.phieusoket15ngay()
        tab_hosokhamchuabenh.donthuoc()
        tab_hosokhamchuabenh.phieucamkettruyenmau(signature)
        # tab_hosokhamchuabenh.phieucamkettta5( signature) # HIS BUG


def pre_run_final_day_check(listing: list[int]):
    _lgr.info("START PRE_RUN_CHECK")
    chieucao_cannang_missing = []
    machanthuong_kemtheo_missing = []
    discharge_date_is_none = []
    appointment_date_is_sat_sun = []

    def check_chieucao_cannang(ma_hs: int):
        with top_chitietthongtin.session():
            if (top_chitietthongtin.get_chieucao() is None) or (
                top_chitietthongtin.get_cannang() is None
            ):
                chieucao_cannang_missing.append(ma_hs)

    def check_machanthuong_kemtheo(ma_hs: int):
        diagnosis = tab_thongtinchung.get_discharge_diagnosis()
        if diagnosis is not None:
            if diagnosis.startswith("S") and not any(
                [d[0] in "WYV" for d in tab_thongtinchung.get_discharge_comorbid()]
            ):
                machanthuong_kemtheo_missing.append(ma_hs)

    def check_discharge_date(ma_hs: int):
        date = tab_thongtinchung.get_discharge_date()
        if date is None:
            discharge_date_is_none.append(ma_hs)

    def check_appointment_date(ma_hs: int):
        date = tab_thongtinchung.get_appointment_date()
        # is saturday / sunday
        if date is not None:
            if date.weekday() in [5, 6]:
                appointment_date_is_sat_sun.append(ma_hs)

    def check(ma_hs: int):
        check_chieucao_cannang(ma_hs)
        check_machanthuong_kemtheo(ma_hs)
        check_discharge_date(ma_hs)
        check_appointment_date(ma_hs)

    try:
        with create_connection() as con:
            first_patient(con, listing[0])
            check(listing[0])
            for ma_hs in listing[1:]:
                next_patient(con, ma_hs)
                check(ma_hs)

    finally:
        is_ok = True
        if len(chieucao_cannang_missing) > 0:
            messagebox.showwarning(
                message="Thiếu chiều cao cân nặng ở chi tiết thông tin:\n"
                + "\n".join([str(x) for x in chieucao_cannang_missing])
            )
            is_ok = False
        if len(machanthuong_kemtheo_missing) > 0:
            messagebox.showwarning(
                message="Thiếu mã chấn thương kèm theo:\n"
                + "\n".join([str(x) for x in machanthuong_kemtheo_missing])
            )
            is_ok = False
        if len(discharge_date_is_none) > 0:
            messagebox.showwarning(
                message="Thiếu ngày ra viện:\n"
                + "\n".join([str(x) for x in discharge_date_is_none])
            )
            is_ok = False
        if len(appointment_date_is_sat_sun) > 0:
            messagebox.showwarning(
                message="Ngày tái khám T7 CN:\n"
                + "\n".join([str(x) for x in appointment_date_is_sat_sun])
            )
            is_ok = False
        _lgr.info("END PRE_RUN_CHECK")
        return is_ok
