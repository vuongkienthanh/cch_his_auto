import tkinter as tk
from tkinter import messagebox
import time
import datetime as dt

from cch_his_auto.app import PROFILE_PATH

from cch_his_auto.common_ui.user_frame import UsernamePasswordDeptFrame
from cch_his_auto.common_ui.button_frame import ButtonFrame, RunConfig


from cch_his_auto_lib.driver import start_driver
from cch_his_auto_lib.action import auth
from cch_his_auto_lib.action import danhsachhoichan

from . import config


TITLE = "TEST"


class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        info = tk.LabelFrame(self, text="Thông tin đăng nhập")
        bacsi = UsernamePasswordDeptFrame(info, text="Bác sĩ ký tên")
        bacsi.grid(row=0, column=0)
        info.grid(row=0, column=0, sticky="N", pady=20)

        button_frame = ButtonFrame(self)
        button_frame.grid(row=0, column=1, rowspan=5, padx=20, sticky="S", pady=(0, 20))

        def load():
            cfg = config.load()

            bacsi.set_name(cfg["username"])
            bacsi.set_password(cfg["password"])
            bacsi.set_department(cfg["department"])

            button_frame.load_config()

        def get_config() -> config.Config:
            return {
                "username": bacsi.get_name(),
                "password": bacsi.get_password(),
                "department": bacsi.get_department(),
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

    with start_driver(headless=run_cfg["headless"], profile_path=PROFILE_PATH) as d:
        with auth.session(d, cfg["username"], cfg["password"], cfg["department"]):
            danhsachhoichan.load(d)
            danhsachhoichan.set_date(d, dt.date.today())
            danhsachhoichan.set_dept(d, cfg["department"])
            time.sleep(5)  # no UI change
            danhsachhoichan.iterate_all_and_do(
                d, danhsachhoichan.open_BBHC_editor, lambda d: print("ASD")
            )
            time.sleep(100)

    messagebox.showinfo(message="finish")
