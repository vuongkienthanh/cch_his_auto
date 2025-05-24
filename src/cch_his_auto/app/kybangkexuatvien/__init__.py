import sqlite3
import tkinter as tk
from tkinter import messagebox, scrolledtext

from cch_his_auto.app import PROFILE_PATH
from cch_his_auto.global_db import create_connection
from cch_his_auto.common_ui.staff_info import UsernamePasswordDeptFrame
from cch_his_auto.common_ui.button_frame import ButtonFrame, RunConfig, setLogLevel
from cch_his_auto.common_tasks.signature import try_get_signature
from cch_his_auto.common_tasks.navigation import first_patient, next_patient

from . import config

from cch_his_auto_lib.driver import start_global_driver
from cch_his_auto_lib.tasks.auth import session
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.bot_indieuduong import (
    sign_bangkechiphiBHYT,
)


TITLE = "Ký bảng kê xuất viện"


class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        info = tk.LabelFrame(self, text="Thông tin đăng nhập")
        staff = UsernamePasswordDeptFrame(info, text="Nhân viên")
        staff.grid(row=0, column=0)
        info.grid(row=0, column=0, sticky="N", pady=20)

        mainframe = tk.Frame(self)
        mainframe.grid(row=1, column=0, sticky="NSEW")
        tk.Label(mainframe, text="Danh sách mã hồ sơ:", anchor="w").grid(
            row=0, column=0, padx=20, sticky="NEW"
        )
        listing = scrolledtext.ScrolledText(mainframe)
        listing.grid(row=1, column=0, padx=20, sticky="NSEW")

        button_frame = ButtonFrame(self)
        button_frame.grid(row=0, column=1, rowspan=2, padx=20, sticky="S", pady=(0, 20))

        def load():
            cfg = config.load()

            staff.set_username(cfg["username"])
            staff.set_password(cfg["password"])
            staff.set_department(cfg["department"])

            listing.delete("1.0", "end")
            listing.insert("1.0", cfg["listing"])

            button_frame.load_config()

        def get_config() -> config.Config:
            return {
                "username": staff.get_username(),
                "password": staff.get_password(),
                "department": staff.get_department(),
                "listing": listing.get("1.0", "end"),
            }

        def save():
            if messagebox.askyesno(message="Save?"):
                config.save(get_config())
                button_frame.save_config()
                messagebox.showinfo(message="Đã lưu")

        button_frame.bind_load(load)
        button_frame.bind_save(save)
        button_frame.bind_run(lambda: run(get_config(), button_frame.get_config()))


def run(cf: config.Config, run_cfg: RunConfig):
    listing = [int(ma_hs) for ma_hs in cf["listing"].strip().splitlines()]
    if len(listing) == 0:
        messagebox.showerror(message="không có bệnh nhân")
        return

    setLogLevel(run_cfg)
    with start_global_driver(headless=run_cfg["headless"], profile_path=PROFILE_PATH):
        with session(cf["username"], cf["password"], cf["department"]):
            with create_connection() as con:
                ma_hs = listing.pop()
                first_patient(con, ma_hs)
                process(con, ma_hs)

                while len(listing) > 0:
                    ma_hs = listing.pop()
                    next_patient(con, ma_hs)
                    process(con, ma_hs)
    messagebox.showinfo(message="finish")


def process(con: sqlite3.Connection, ma_hs: int):
    if signature := try_get_signature(con, ma_hs):
        sign_bangkechiphiBHYT(True, signature)
