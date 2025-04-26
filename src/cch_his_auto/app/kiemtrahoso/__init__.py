import tkinter as tk
from tkinter import messagebox, scrolledtext

from cch_his_auto.app import PROFILE_PATH
from cch_his_auto.global_db import create_connection
from cch_his_auto.common_ui.staff_info import UsernamePasswordDeptFrame
from cch_his_auto.common_ui.button_frame import ButtonFrame, RunConfig, setLogLevel
from cch_his_auto.common_tasks.navigation import first_patient, next_patient
from cch_his_auto.common_tasks.signature import get_signature_from_ctnbnt

from . import config

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tasks import auth, danhsachnguoibenhnoitru
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import (
    tab_thongtinchung,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.tab_thongtinchung import (
    edit_thongtinvaovien,
    edit_thongtinravien,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.upper_patient_info_buttons import (
    chitietthongtin,
    hosobenhan,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.upper_patient_info_buttons.hosobenhan import (
    tab_hosokhamchuabenh,
    tab_mau,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.lower_buttons import (
    sanglocdinhduong,
)


TITLE = "Kiểm tra hồ sơ"
APP_INTRO = """
    Chức năng hiện tại:
        + Mục A, mục B
        + Phiếu chỉ định, tờ điều trị
        + Phiếu CT, MRI
        + Phiếu giải phẫu bệnh
        + Phiếu sàng lọc dinh dưỡng
        + Ký sơ kết 15n
        - Tờ bìa, tờ điều trị XV

    """


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
        tk.Label(
            mainframe,
            text=APP_INTRO,
            justify="left",
            anchor="w",
        ).grid(row=3, column=0, rowspan=4, sticky="SEW", padx=20)

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
    driver = Driver(headless=run_cfg["headless"], profile_path=PROFILE_PATH)

    listing = [int(ma_hs) for ma_hs in cfg["listing"].strip().splitlines()]

    try:
        with auth.session(driver, cfg["username"], cfg["password"], cfg["department"]):
            if cfg["is_final_day"]:
                if not pre_run_final_day_check(driver, listing):
                    return
                process = process_final_day
            else:
                process = process_normal_day
            with create_connection() as con:
                if cfg["discharged"]:
                    danhsachnguoibenhnoitru.filter_trangthainguoibenh(driver, [10])

                ma_hs = listing.pop()
                first_patient(driver, con, ma_hs)
                signature = get_signature_from_ctnbnt(driver, con, ma_hs)
                process(driver, signature)

                while len(listing) > 0:
                    ma_hs = listing.pop()
                    next_patient(driver, con, ma_hs)
                    signature = get_signature_from_ctnbnt(driver, con, ma_hs)
                    process(driver, signature)
    finally:
        driver.quit()
        messagebox.showinfo(message="finish")


def process_normal_day(driver: Driver, signature: str | None):
    admission_date = tab_thongtinchung.get_admission_date(driver)
    discharge_date = tab_thongtinchung.get_discharge_date(driver)
    sanglocdinhduong.add_all_phieusanglocdinhduong(driver, admission_date)

    # điền thông tin nhóm máu
    bloodtype = tab_thongtinchung.get_bloodtype(driver)
    if bloodtype is None:
        with hosobenhan.session(driver, tab_mau.TAB_NUMBER):
            found_bloodtype = tab_mau.get_bloodtype(driver)
        if found_bloodtype is not None:
            with edit_thongtinvaovien.session(driver):
                edit_thongtinvaovien.set_bloodtype(driver, found_bloodtype)

    with hosobenhan.session(driver):
        tab_hosokhamchuabenh.phieuchidinhxetnghiem(driver)
        tab_hosokhamchuabenh.todieutri(driver, discharge_date)
        tab_hosokhamchuabenh.phieuCT(driver, signature)
        tab_hosokhamchuabenh.phieuMRI(driver, signature)
        tab_hosokhamchuabenh.giaiphaubenh(driver)
        tab_hosokhamchuabenh.phieusanglocdinhduong(driver)
        tab_hosokhamchuabenh.phieuchidinhPTTT(driver)
        tab_hosokhamchuabenh.phieusoket15ngay(driver)
        tab_hosokhamchuabenh.phieucamkettruyenmau(driver, signature)
        tab_hosokhamchuabenh.phieucamkettta5(driver, signature)


def process_final_day(driver: Driver, signature: str | None):
    admission_date = tab_thongtinchung.get_admission_date(driver)
    sanglocdinhduong.add_all_phieusanglocdinhduong(driver, admission_date)
    discharge_date = tab_thongtinchung.get_discharge_date(driver)

    # mở rộng chữ viết tắt
    viettat_dict = {
        "hp": "hậu phẫu",
        "pt": "phẫu thuật",
        "nmc": "ngoài màng cứng",
        "dmc": "dưới màng cứng",
    }
    detail = tab_thongtinchung.get_discharge_diagnosis_detail(driver)
    if detail is not None:
        detail = detail.lower()
        for k, v in viettat_dict.items():
            detail = detail.replace(k, v)
        with edit_thongtinravien.session(driver):
            edit_thongtinravien.set_discharge_diagnosis_detail(driver, detail)
    treatment = tab_thongtinchung.get_treatment(driver)
    if treatment is not None:
        treatment = treatment.lower()
        for k, v in viettat_dict.items():
            treatment = treatment.replace(k, v)
        with edit_thongtinravien.session(driver):
            edit_thongtinravien.set_treatment(driver, treatment)

    # điền thông tin nhóm máu
    bloodtype = tab_thongtinchung.get_bloodtype(driver)
    if bloodtype is None:
        with hosobenhan.session(driver, tab_mau.TAB_NUMBER):
            found_bloodtype = tab_mau.get_bloodtype(driver)
        if found_bloodtype is not None:
            with edit_thongtinvaovien.session(driver):
                edit_thongtinvaovien.set_bloodtype(driver, found_bloodtype)

    with hosobenhan.session(driver):
        # tab_hosokhamchuabenh.tobiabenhannhikhoa(driver)
        tab_hosokhamchuabenh.mucAbenhannhikhoa(driver)
        tab_hosokhamchuabenh.mucBtongketbenhan(driver)
        tab_hosokhamchuabenh.phieukhambenhvaovien(driver)
        tab_hosokhamchuabenh.phieuchidinhxetnghiem(driver)
        tab_hosokhamchuabenh.todieutri(driver, discharge_date)
        tab_hosokhamchuabenh.phieuCT(driver, signature)
        tab_hosokhamchuabenh.phieuMRI(driver, signature)
        tab_hosokhamchuabenh.giaiphaubenh(driver)
        tab_hosokhamchuabenh.phieusanglocdinhduong(driver)
        tab_hosokhamchuabenh.phieuchidinhPTTT(driver)
        tab_hosokhamchuabenh.phieusoket15ngay(driver)
        tab_hosokhamchuabenh.donthuoc(driver)
        tab_hosokhamchuabenh.phieucamkettruyenmau(driver, signature)
        tab_hosokhamchuabenh.phieucamkettta5(driver, signature)


def pre_run_final_day_check(driver: Driver, listing: list[int]):
    chieucao_cannang_missing = []
    machanthuong_kemtheo_missing = []
    discharge_date_is_none = []
    appointment_date_is_sat_sun = []

    def check_chieucao_cannang(driver: Driver, ma_hs: int):
        with chitietthongtin.session(driver):
            if (chitietthongtin.get_chieucao(driver) is None) or (
                chitietthongtin.get_cannang(driver) is None
            ):
                chieucao_cannang_missing.append(ma_hs)

    def check_machanthuong_kemtheo(driver: Driver, ma_hs: int):
        diagnosis = tab_thongtinchung.get_discharge_diagnosis(driver)
        if diagnosis is not None:
            if diagnosis.startswith("S") and not any(
                [
                    d[0] in "WYV"
                    for d in tab_thongtinchung.get_discharge_comorbid(driver)
                ]
            ):
                machanthuong_kemtheo_missing.append(ma_hs)

    def check_discharge_date(driver: Driver, ma_hs: int):
        date = tab_thongtinchung.get_discharge_date(driver)
        if date is None:
            discharge_date_is_none.append(ma_hs)

    def check_appointment_date(driver: Driver, ma_hs: int):
        date = tab_thongtinchung.get_appointment_date(driver)
        # is saturday / sunday
        if date is not None:
            if date.weekday() in [5, 6]:
                appointment_date_is_sat_sun.append(ma_hs)

    def check(driver: Driver, ma_hs: int):
        check_chieucao_cannang(driver, ma_hs)
        check_machanthuong_kemtheo(driver, ma_hs)
        check_discharge_date(driver, ma_hs)
        check_appointment_date(driver, ma_hs)

    try:
        with create_connection() as con:
            first_patient(driver, con, listing[0])
            check(driver, listing[0])
            for ma_hs in listing[1:]:
                next_patient(driver, con, ma_hs)
                check(driver, ma_hs)

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
        driver.goto(danhsachnguoibenhnoitru.URL)
        return is_ok
