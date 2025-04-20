import logging
import tkinter as tk
from tkinter import messagebox

from . import config
from .patient_list import PatientFrame

from cch_his_auto.driver import Driver
from cch_his_auto.tasks.auth import session
from cch_his_auto.tasks.todieutri import ingiayto as igt
from cch_his_auto.tasks.chitietnguoibenhnoitru import hosobenhan

from cch_his_auto.app import PROFILE_PATH
from cch_his_auto.app.global_db import create_connection, get_url_from_db
from cch_his_auto.app.common_ui.staff_info import UsernamePasswordFrame
from cch_his_auto.app.common_ui.button_frame import ButtonFrame2, RunConfig, setLogLevel
from cch_his_auto.app.common_tasks.signature import get_signature_from_elsewhere

TITLE = "Ký tờ điều trị hằng ngày"
_logger = logging.getLogger().getChild("app")


class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        info = tk.LabelFrame(self, text="Thông tin đăng nhập")
        bacsi = UsernamePasswordFrame(info, text="Bác sĩ")
        dieuduong = UsernamePasswordFrame(info, text="Điều dưỡng")
        bacsi.grid(row=0, column=0)
        dieuduong.grid(row=0, column=1)
        dept_var = tk.StringVar()
        tk.Label(info, text="Khoa lâm sàng:", justify="right").grid(
            row=1, column=0, sticky="E"
        )
        tk.Entry(info, textvariable=dept_var).grid(row=1, column=1, sticky="W")
        info.grid(row=0, column=0, sticky="N", pady=20)

        mainframe = PatientFrame(self)
        mainframe.grid(row=1, column=0, sticky="NSEW")

        button_frame = ButtonFrame2(self, custom_text="Add")
        button_frame.grid(row=0, column=1, rowspan=2, padx=20, sticky="S", pady=(0, 20))

        def load():
            cfg = config.load()

            bacsi.set_username(cfg["bacsi"]["username"])
            bacsi.set_password(cfg["bacsi"]["password"])
            dieuduong.set_username(cfg["dieuduong"]["username"])
            dieuduong.set_password(cfg["dieuduong"]["password"])
            dept_var.set(cfg["department"])

            mainframe.clear()
            for p in cfg["patients"]:
                mainframe.add_patient(p)

            button_frame.load_config()

        def get_config() -> config.Config:
            return {
                "bacsi": {
                    "username": bacsi.get_username(),
                    "password": bacsi.get_password(),
                },
                "dieuduong": {
                    "username": dieuduong.get_username(),
                    "password": dieuduong.get_password(),
                },
                "department": dept_var.get(),
                "patients": mainframe.get_patients(),
            }

        def save():
            if messagebox.askyesno(message="Save?"):
                config.save(get_config())
                button_frame.save_config()
                messagebox.showinfo(message="Đã lưu")

        button_frame.bind_load(load)
        button_frame.bind_save(save)
        button_frame.bind_custom(mainframe.add_new)
        button_frame.bind_run(lambda: run(get_config(), button_frame.get_config()))


def run(cfg: config.Config, run_cfg: RunConfig):
    if not config.is_patient_list_valid(cfg):
        messagebox.showerror(message="không có bệnh nhân")
        return

    setLogLevel(run_cfg)
    driver = Driver(headless=run_cfg["headless"], profile_path=PROFILE_PATH)
    try:
        bs, dd = config.is_bs_valid(cfg), config.is_dd_valid(cfg)
        match (bs, dd):
            case (True, True):
                with session(
                    driver,
                    cfg["bacsi"]["username"],
                    cfg["bacsi"]["password"],
                    cfg["department"],
                ):
                    run_bs(driver, cfg)
                with session(
                    driver,
                    cfg["dieuduong"]["username"],
                    cfg["dieuduong"]["password"],
                    cfg["department"],
                ):
                    run_dd(driver, cfg)
                    run_bn(driver, cfg)
            case (True, False):
                with session(
                    driver,
                    cfg["bacsi"]["username"],
                    cfg["bacsi"]["password"],
                    cfg["department"],
                ):
                    run_bs(driver, cfg)
                    run_bn(driver, cfg)
                messagebox.showwarning(message="chưa nhập điều dưỡng")
            case (False, True):
                with session(
                    driver,
                    cfg["dieuduong"]["username"],
                    cfg["dieuduong"]["password"],
                    cfg["department"],
                ):
                    run_dd(driver, cfg)
                    run_bn(driver, cfg)
                messagebox.showwarning(message="chưa nhập bác sĩ")
            case _:
                messagebox.showwarning(message="chưa nhập bác sĩ, điều dưỡng")
    finally:
        driver.quit()
        messagebox.showinfo(message="finish")


def run_bs(driver: Driver, cfg: config.Config):
    for p in cfg["patients"]:
        driver.goto(p["url"])
        _logger.info(f"patient: {driver.waiting('.name span').text}")

        if p["ky_xetnghiem"]:
            igt.sign_phieuchidinh(driver)
        if p["ky_ct"]:
            driver.clicking(".right button:nth-child(2)")
            hosobenhan.open_dialog(driver)
            hosobenhan.phieuCT(driver)
            hosobenhan.close_dialog(driver)
            driver.goto(p["url"])
        if p["ky_todieutri"]:
            igt.sign_todieutri(driver)
        if any(p["ky_3tra"]["bacsi"]):
            igt.sign_phieuthuchienylenh_bs(driver, p["ky_3tra"]["bacsi"])


def run_dd(driver: Driver, cfg: config.Config):
    for p in cfg["patients"]:
        driver.goto(p["url"])
        _logger.info(f"patient: {driver.waiting('.name span').text}")
        if any(p["ky_3tra"]["dieuduong"]):
            igt.sign_phieuthuchienylenh_dd(driver, p["ky_3tra"]["dieuduong"])


def run_bn(driver: Driver, cfg: config.Config):
    with create_connection() as con:
        for p in cfg["patients"]:
            driver.goto(p["url"])
            _logger.info(f"patient: {driver.waiting('.name span').text}")
            ma_hs = int(
                driver.waiting(
                    ".patient-information .additional-item:nth-child(2) .info",
                    "ma ho so",
                ).text
            )
            if signature := get_signature_from_elsewhere(driver, con, ma_hs):
                if any(p["ky_3tra"]["benhnhan"]):
                    igt.sign_phieuthuchienylenh_bn(
                        driver, p["ky_3tra"]["benhnhan"], signature
                    )
