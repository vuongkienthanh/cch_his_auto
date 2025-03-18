import os.path
import sqlite3
import tkinter as tk
from tkinter import messagebox, scrolledtext

TITLE = "Ký bảng kê xuất viện"
APP_PATH = os.path.dirname(os.path.abspath(__file__))

from . import config
from cch_his_auto.app.common_tasks.navigation import first_patient, next_patient
from cch_his_auto.app.common_tasks.signature import get_signature_wo_goback
from cch_his_auto.driver import Driver
from cch_his_auto.app.ma_hs_db import create_connection
from cch_his_auto.tasks.chitietnguoibenhnoitru.indieuduong import bangkechiphiBHYT

class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        from cch_his_auto.app.common_ui.staff_info import UsernamePasswordDeptFrame

        info = tk.LabelFrame(self, text="Thông tin đăng nhập")
        staff = UsernamePasswordDeptFrame(info, text="Nhân viên")
        staff.grid(row=0, column=0)
        headless_var = tk.BooleanVar()
        headless_btn = tk.Checkbutton(
            info, variable=headless_var, text="Headless Chrome"
        )
        headless_btn.grid(row=1, column=0, pady=5)
        info.grid(row=0, column=0, sticky="N", pady=20)

        mainframe = tk.Frame(self)
        mainframe.grid(row=1, column=0, sticky="NSEW")
        tk.Label(mainframe, text="Danh sách mã hồ sơ:", anchor="w").grid(
            row=0, column=0, padx=20, sticky="NEW"
        )
        dsmahs = scrolledtext.ScrolledText(mainframe)
        dsmahs.grid(row=1, column=0, padx=20, sticky="NSEW")

        def load():
            cf = config.load()
            headless_var.set(cf["headless"])
            staff.set_username(cf["username"])
            staff.set_password(cf["password"])
            staff.set_department(cf["department"])
            dsmahs.delete("1.0", "end")
            dsmahs.insert("1.0", cf["ds_ma_hs"])

        def get_config() -> config.Config:
            return {
                "headless": headless_var.get(),
                "username": staff.get_username(),
                "password": staff.get_password(),
                "department": staff.get_department(),
                "ds_ma_hs": dsmahs.get("1.0", "end"),
            }

        def save():
            config.save(get_config())
            if messagebox.askyesno(message="Save?"):
                messagebox.Message(default=messagebox.OK, message="Đã lưu").show()

        btns = tk.Frame(self)
        load_btn = tk.Button(btns, text="Load", command=load, width=10)
        load_btn.grid(row=0, column=0, pady=5)
        save_btn = tk.Button(btns, text="Save", command=save, width=10)
        save_btn.grid(row=1, column=0, pady=5)
        run_btn = tk.Button(
            btns,
            text="RUN",
            command=lambda: run(get_config()),
            width=10,
            bg="#ff0073",
            fg="#ffffff",
        )
        run_btn.grid(row=2, column=0, pady=5)
        btns.grid(row=0, column=1, rowspan=2, padx=20, sticky="S", pady=(0, 20))

def run(cf: config.Config):
    from cch_his_auto.tasks.auth import login_then_choose_dept
    from cch_his_auto.app import PROFILE_PATH

    listing = [int(ma_hs) for ma_hs in cf["ds_ma_hs"].strip().splitlines()]

    driver = Driver(headless=cf["headless"], profile_path=PROFILE_PATH)

    # set up HIS
    login_then_choose_dept(driver, cf["username"], cf["password"], cf["department"])

    con = create_connection()

    ma_hs = listing.pop()
    first_patient(driver, ma_hs)
    process(driver, con, ma_hs)

    while len(listing) > 0:
        ma_hs = listing.pop()
        next_patient(driver, ma_hs)
        process(driver, con, ma_hs)

    con.close()
    driver.quit()

def process(driver: Driver, con: sqlite3.Connection, ma_hs: int):
    signature = get_signature_wo_goback(driver, con, ma_hs)
    bangkechiphiBHYT.open(driver)
    bangkechiphiBHYT.goto_iframe(driver)
    bangkechiphiBHYT.sign_staff(driver)
    bangkechiphiBHYT.sign_patient(driver, signature)
    bangkechiphiBHYT.goout_iframe(driver)
    bangkechiphiBHYT.close(driver)
