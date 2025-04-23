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
from cch_his_auto_lib.tasks import auth, danhsachnguoibenhnoitru, chitietnguoibenhnoitru
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import (
    hosobenhan,
    sanglocdinhduong,
    chitietthongtin,
    thongtinravien,
    thongtinvaovien,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.hosobenhan import (
    tab_hosokhamchuabenh,
    tab_mau,
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
        run_check_btn = tk.Button(mainframe, text="Kiểm tra trước")
        run_check_btn.grid(row=3, column=1, padx=20)

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
        run_check_btn.configure(
            command=lambda: run_check(get_config(), button_frame.get_config())
        )


def run(cfg: config.Config, run_cfg: RunConfig):
    listing = [int(ma_hs) for ma_hs in cfg["listing"].strip().splitlines()]
    if len(listing) == 0:
        messagebox.showerror(message="không có bệnh nhân")
        return

    setLogLevel(run_cfg)
    driver = Driver(headless=run_cfg["headless"], profile_path=PROFILE_PATH)
    if cfg["is_final_day"]:
        process = process_final_day
    else:
        process = process_normal_day
    try:
        with create_connection() as con:
            with auth.session(
                driver, cfg["username"], cfg["password"], cfg["department"]
            ):
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
    admission_date = chitietnguoibenhnoitru.get_admission_date(driver)
    discharge_date = chitietnguoibenhnoitru.get_discharge_date(driver)
    sanglocdinhduong.add_all_phieusanglocdinhduong(driver, admission_date)

    with hosobenhan.session(driver):
        tab_hosokhamchuabenh.phieuchidinhxetnghiem(driver)
        tab_hosokhamchuabenh.todieutri(driver, discharge_date)
        tab_hosokhamchuabenh.phieuCT(driver, signature)
        tab_hosokhamchuabenh.phieuMRI(driver, signature)
        tab_hosokhamchuabenh.giaiphaubenh(driver)
        tab_hosokhamchuabenh.phieusanglocdinhduong(driver)
        tab_hosokhamchuabenh.phieuchidinhPTTT(driver)
        tab_hosokhamchuabenh.phieusoket15ngay(driver)


def process_final_day(driver: Driver, signature: str | None):
    admission_date = chitietnguoibenhnoitru.get_admission_date(driver)
    sanglocdinhduong.add_all_phieusanglocdinhduong(driver, admission_date)

    # kiểm tra ngày xuất viện
    discharge_date = chitietnguoibenhnoitru.get_discharge_date(driver)
    if discharge_date is None:
        messagebox.showwarning("Chưa có ngày xuất viện")
        return

    # kiểm tra viết tắt
    detail = chitietnguoibenhnoitru.get_discharge_diagnosis_detail(driver)
    if detail is not None:
        detail = detail.lower()
        if any([viettat in detail for viettat in ["hp", "nmc", "dmc"]]):
            detail = detail.replace("hp", "hậu phẫu")
            detail = detail.replace("nmc", "ngoài màng cứng")
            detail = detail.replace("dmc", "dưới màng cứng")
            with thongtinravien.session(driver):
                thongtinravien.set_discharge_diagnosis_detail(driver, detail)

    # điền thông tin nhóm máu
    bloodtype = chitietnguoibenhnoitru.get_bloodtype(driver)
    if bloodtype is None:
        with hosobenhan.session(driver, tab_mau.TAB_NUNMBER):
            found_bloodtype = tab_mau.get_bloodtype(driver)
        if found_bloodtype is not None:
            with thongtinvaovien.session(driver):
                thongtinvaovien.set_bloodtype(driver, found_bloodtype)

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


def run_check(cfg: config.Config, run_cfg: RunConfig):
    listing = [int(ma_hs) for ma_hs in cfg["listing"].strip().splitlines()]
    if len(listing) == 0:
        messagebox.showerror(message="không có bệnh nhân")
        return

    chieucao_cannang_missing = []
    machanthuong_kemtheo_missing = []
    discharge_date_is_sat_sun = []

    def check_chieucao_cannang(driver: Driver, ma_hs: int):
        with chitietthongtin.session(driver):
            if (chitietthongtin.get_chieucao(driver) is None) or (
                chitietthongtin.get_cannang(driver) is None
            ):
                chieucao_cannang_missing.append(ma_hs)

    def check_machanthuong_kemtheo(driver: Driver, ma_hs: int):
        diagnosis = chitietnguoibenhnoitru.get_discharge_diagnosis(driver)
        if diagnosis is not None:
            if diagnosis.startswith("S") and any(
                [
                    d[0] not in "WYV"
                    for d in chitietnguoibenhnoitru.get_discharge_comorbid(driver)
                ]
            ):
                machanthuong_kemtheo_missing.append(ma_hs)

    def check_discharge_date_is_sat_sun(driver: Driver, ma_hs: int):
        date = chitietnguoibenhnoitru.get_discharge_date(driver)
        if date is not None:
            if date.weekday() in [5, 6]:
                discharge_date_is_sat_sun.append(ma_hs)

    def check(driver: Driver, ma_hs: int):
        check_chieucao_cannang(driver, ma_hs)
        check_machanthuong_kemtheo(driver, ma_hs)
        check_discharge_date_is_sat_sun(driver, ma_hs)

    setLogLevel(run_cfg)
    driver = Driver(headless=run_cfg["headless"], profile_path=PROFILE_PATH)
    try:
        with create_connection() as con:
            with auth.session(
                driver, cfg["username"], cfg["password"], cfg["department"]
            ):
                ma_hs = listing.pop()
                first_patient(driver, con, ma_hs)
                check(driver, ma_hs)
                while len(listing) > 0:
                    ma_hs = listing.pop()
                    next_patient(driver, con, ma_hs)
                    check(driver, ma_hs)

    finally:
        driver.quit()
        if len(chieucao_cannang_missing) > 0:
            messagebox.showwarning(
                message="Thiếu chiều cao cân nặng ở chi tiết thông tin:\n"
                + "\n".join([str(x) for x in chieucao_cannang_missing])
            )
        if len(machanthuong_kemtheo_missing) > 0:
            messagebox.showwarning(
                message="Thiếu mã chấn thương kèm theo:\n"
                + "\n".join([str(x) for x in machanthuong_kemtheo_missing])
            )
        messagebox.showinfo(message="finish")
