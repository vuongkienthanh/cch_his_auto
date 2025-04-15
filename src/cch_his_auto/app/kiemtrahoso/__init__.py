import tkinter as tk
from tkinter import messagebox, scrolledtext

from . import config

from cch_his_auto.driver import Driver
from cch_his_auto.tasks.auth import session
from cch_his_auto.tasks.chitietnguoibenhnoitru import hosobenhan, sanglocdinhduong
from cch_his_auto.tasks import danhsachnguoibenhnoitru

from cch_his_auto.app import PROFILE_PATH
from cch_his_auto.app.global_db import create_connection
from cch_his_auto.app.common_ui.staff_info import UsernamePasswordDeptFrame
from cch_his_auto.app.common_ui.button_frame import ButtonFrame, RunConfig, setLogLevel
from cch_his_auto.app.common_tasks.navigation import first_patient, next_patient
from cch_his_auto.app.common_tasks.signature import get_signature_from_ctnbnt

TITLE = "Kiểm tra hồ sơ"
APP_INTRO = """
    Chức năng hiện tại:
        + Tờ bìa, mục A, mục B
        + phiếu chỉ định, tờ điều trị
        + Phiếu CT, MRI
        + Phiếu giải phẫu bệnh
        + Phiếu sàng lọc dinh dưỡng
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
        ).grid(row=2, column=0, sticky="SEW", padx=20, columnspan=2)

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
                messagebox.showinfo(message="Đã lưu")

        button_frame.bind_load(load)
        button_frame.bind_save(save)
        button_frame.bind_run(lambda: run(get_config(), button_frame.get_config()))


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
            with session(driver, cfg["username"], cfg["password"], cfg["department"]):
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
    sanglocdinhduong.complete_sanglocdinhduong(driver)

    hosobenhan.open_dialog(driver)
    hosobenhan.phieuchidinhxetnghiem(driver)
    hosobenhan.todieutri(driver)
    hosobenhan.phieuCT(driver)
    hosobenhan.phieuMRI(driver, signature)
    hosobenhan.giaiphaubenh(driver)
    hosobenhan.phieusanglocdinhduong(driver)
    hosobenhan.close_dialog(driver)


def process_final_day(driver: Driver, signature: str | None):
    sanglocdinhduong.complete_sanglocdinhduong(driver)

    hosobenhan.open_dialog(driver)
    hosobenhan.tobiabenhannhikhoa(driver)
    hosobenhan.mucAbenhannhikhoa(driver)
    hosobenhan.mucBtongketbenhan(driver)
    hosobenhan.phieuchidinhxetnghiem(driver)
    hosobenhan.todieutri(driver)
    hosobenhan.phieuCT(driver)
    hosobenhan.phieuMRI(driver, signature)
    hosobenhan.giaiphaubenh(driver)
    hosobenhan.phieusanglocdinhduong(driver)
    hosobenhan.close_dialog(driver)
