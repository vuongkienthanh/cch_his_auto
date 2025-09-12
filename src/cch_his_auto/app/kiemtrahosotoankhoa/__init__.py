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
        user = UsernamePasswordDeptFrame(info, text="Bác sĩ ký tên")
        user.grid(row=0, column=0)
        info.grid(row=0, column=0, sticky="N", pady=20)

        dinhduong_var = tk.BooleanVar()
        nhommau_var = tk.BooleanVar()

        optionframe = tk.Frame(self)
        optionframe.grid(row=1, column=0, sticky="NSEW", padx=10)

        tk.Checkbutton(
            optionframe, text="Phiếu dinh dưỡng", variable=dinhduong_var, justify="left"
        ).grid(row=0, column=0, padx=5, sticky="W")
        tk.Checkbutton(
            optionframe, text="Nhóm máu", variable=nhommau_var, justify="left"
        ).grid(row=1, column=0, padx=5, sticky="W")

        button_frame = ButtonFrame(self)
        button_frame.grid(row=0, column=1, rowspan=5, padx=20, sticky="S", pady=(0, 20))

        def load():
            cfg = Config.load()

            user.set_user(cfg.user)
            user.set_department(cfg.department)
            dinhduong_var.set(cfg.dinhduong)
            nhommau_var.set(cfg.nhommau)

            button_frame.load_config()

        def get_config() -> Config:
            return Config(
                user.get_user(),
                user.get_department(),
                dinhduong_var.get(),
                nhommau_var.get(),
            )

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
        return
    if not cfg.user.is_valid():
        return

    processes = []
    if cfg.nhommau:
        processes.append(nhommau)
    if cfg.dinhduong:
        processes.append(dinhduong)

    with start_driver(headless=run_cfg.headless, profile_path=PROFILE_PATH) as d:
        with auth.session(d, cfg.user.name, cfg.user.password, cfg.department):
            danhsachnguoibenhnoitru.load(d)
            danhsachnguoibenhnoitru.iterate_all_and_do(
                d, lambda d: [m.run(d) for m in processes]
            )

    messagebox.showinfo(message="finish")
