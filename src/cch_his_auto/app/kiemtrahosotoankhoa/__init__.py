import tkinter as tk
from dataclasses import astuple
from tkinter import messagebox

from cch_his_auto.app import PROFILE_PATH

from cch_his_auto.common_ui.user_frame import UsernamePasswordDeptFrame
from cch_his_auto.common_ui.button_frame import ButtonFrame, RunConfig


from cch_his_auto_lib.driver import start_driver
from cch_his_auto_lib.action import danhsachnguoibenhnoitru
from cch_his_auto_lib.action import auth
from cch_his_auto_lib.common_tasks import iterate_all_patient

from . import dinhduong, nhommau, kytenhosobenhan
from .config import Config, Kytenhosobenhan


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

        kytenhosobenhan_var = tk.BooleanVar()
        mucAbenhannhikhoa_var = tk.BooleanVar()
        phieukhambenhvaovien_var = tk.BooleanVar()
        phieusanglocdinhduong_var = tk.BooleanVar()
        phieusoket15ngay_var = tk.BooleanVar()
        phieuchidinhxetnghiem_var = tk.BooleanVar()
        phieuCT_var = tk.BooleanVar()
        phieuMRI_var = tk.BooleanVar()
        donthuoc_var = tk.BooleanVar()
        todieutri_var = tk.BooleanVar()

        def toggle_kyhosobenhan():
            val = kytenhosobenhan_var.get()
            mucAbenhannhikhoa_var.set(val)
            phieukhambenhvaovien_var.set(val)
            phieusanglocdinhduong_var.set(val)
            phieusoket15ngay_var.set(val)
            phieuchidinhxetnghiem_var.set(val)
            phieuCT_var.set(val)
            phieuMRI_var.set(val)
            donthuoc_var.set(val)
            todieutri_var.set(val)

        optionframe = tk.Frame(self)
        optionframe.grid(row=1, column=0, sticky="NSEW", padx=10)

        tk.Checkbutton(
            optionframe, text="Phiếu dinh dưỡng", variable=dinhduong_var, justify="left"
        ).grid(row=0, column=0, padx=5, sticky="W")
        tk.Checkbutton(
            optionframe, text="Nhóm máu", variable=nhommau_var, justify="left"
        ).grid(row=1, column=0, padx=5, sticky="W")

        tk.Checkbutton(
            optionframe,
            text="Ký tên hồ sơ bệnh án",
            variable=kytenhosobenhan_var,
            justify="left",
            command=toggle_kyhosobenhan,
        ).grid(row=2, column=0, padx=5, sticky="W")
        for i, (a, b) in enumerate(
            [
                ("mục A bệnh án nhi khoa", mucAbenhannhikhoa_var),
                ("phiếu khám bệnh vào viện", phieukhambenhvaovien_var),
                ("phiếu sàng lọc dinh dưỡng", phieusanglocdinhduong_var),
                ("phiếu sơ kết 15 ngày", phieusoket15ngay_var),
                ("phiếu chỉ định xét nghiệm", phieuchidinhxetnghiem_var),
                ("phiếu CT", phieuCT_var),
                ("phiếu MRI", phieuMRI_var),
                ("đơn thuốc", donthuoc_var),
                ("tờ điều trị", todieutri_var),
            ],
            4,
        ):
            tk.Checkbutton(
                optionframe,
                text=a,
                variable=b,
                justify="left",
            ).grid(row=i, column=0, padx=30, sticky="W")

        button_frame = ButtonFrame(self)
        button_frame.grid(row=0, column=1, rowspan=5, padx=20, sticky="S", pady=(0, 20))

        def load():
            cfg = Config.load()

            user.set_user(cfg.user)
            user.set_department(cfg.department)
            dinhduong_var.set(cfg.dinhduong)
            nhommau_var.set(cfg.nhommau)
            mucAbenhannhikhoa_var.set(cfg.kytenhosobenhan.mucAbenhannhikhoa)
            phieukhambenhvaovien_var.set(cfg.kytenhosobenhan.phieukhambenhvaovien)
            phieusanglocdinhduong_var.set(cfg.kytenhosobenhan.phieusanglocdinhduong)
            phieusoket15ngay_var.set(cfg.kytenhosobenhan.phieusoket15ngay)
            phieuchidinhxetnghiem_var.set(cfg.kytenhosobenhan.phieuchidinhxetnghiem)
            phieuCT_var.set(cfg.kytenhosobenhan.phieuCT)
            phieuMRI_var.set(cfg.kytenhosobenhan.phieuMRI)
            donthuoc_var.set(cfg.kytenhosobenhan.donthuoc)
            todieutri_var.set(cfg.kytenhosobenhan.todieutri)
            kytenhosobenhan_var.set(all(astuple(cfg.kytenhosobenhan)))

            button_frame.load_config()

        def get_config() -> Config:
            return Config(
                user.get_user(),
                user.get_department(),
                dinhduong_var.get(),
                nhommau_var.get(),
                Kytenhosobenhan(
                    mucAbenhannhikhoa_var.get(),
                    phieukhambenhvaovien_var.get(),
                    phieusanglocdinhduong_var.get(),
                    phieusoket15ngay_var.get(),
                    phieuchidinhxetnghiem_var.get(),
                    phieuCT_var.get(),
                    phieuMRI_var.get(),
                    donthuoc_var.get(),
                    todieutri_var.get(),
                ),
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

    with start_driver(headless=run_cfg.headless, profile_path=PROFILE_PATH) as d:
        with auth.session(d, cfg.user.name, cfg.user.password, cfg.department):
            danhsachnguoibenhnoitru.load(d)
            iterate_all_patient(
                d,
                lambda d: [
                    m.run(d, cfg) for m in [nhommau, dinhduong, kytenhosobenhan]
                ],
            )

    messagebox.showinfo(message="finish")
