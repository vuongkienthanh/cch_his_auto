from functools import partial
import tkinter as tk
from tkinter import messagebox

from cch_his_auto.app import PROFILE_PATH

from cch_his_auto.common_ui.user_frame import UsernamePasswordDeptFrame
from cch_his_auto.common_ui.button_frame import ButtonFrame, RunConfig


from cch_his_auto_lib.driver import start_driver
from cch_his_auto_lib.action import danhsachnguoibenhnoitru
from cch_his_auto_lib.action import auth

from . import dinhduong, nhommau
from .config import Config


TITLE = "Kiểm tra hồ sơ toàn khoa"


class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        info = tk.LabelFrame(self, text="Thông tin đăng nhập")
        bacsi = UsernamePasswordDeptFrame(info, text="Bác sĩ ký tên")
        bacsi.grid(row=0, column=0)
        info.grid(row=0, column=0, sticky="N", pady=20)

        optionframe = tk.Frame(self)
        optionframe.grid(row=1, column=0, sticky="NSEW", padx=10)

        button_frame = ButtonFrame(self)
        button_frame.grid(row=0, column=1, rowspan=5, padx=20, sticky="S", pady=(0, 20))

        def load():
            cfg = Config.load()

            bacsi.set_user(cfg.user)
            bacsi.set_department(cfg.department)

            button_frame.load_config()

        def get_config() -> Config:
            return Config (
            "user": bacsi.get_user(),
            "department": bacsi.get_department(),
            "listing": (),)


        def save():
            if messagebox.askyesno(message="Save?"):
                get_config().save()
                button_frame.save_config()
                messagebox.showinfo(message="Đã lưu")

        button_frame.bind_load(load)
        button_frame.bind_save(save)
        button_frame.bind_run(lambda: run(get_config(), button_frame.get_config()))


def run(cfg: Config, run_cfg: RunConfig):
    if not cfg.is_valid():
        messagebox.showerror(message="chưa đủ thông tin")
        return

    messagebox.showinfo(message="finish")
