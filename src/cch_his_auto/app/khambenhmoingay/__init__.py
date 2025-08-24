import tkinter as tk
from tkinter import messagebox, ttk
import datetime as dt
from typing import Literal, get_args

from cch_his_auto.app import PROFILE_PATH, _lgr
from cch_his_auto.global_db import create_connection
from cch_his_auto.common_ui.staff_info import UsernamePasswordFrame
from cch_his_auto.common_ui.button_frame import ButtonFrame, RunConfig
from cch_his_auto.common_tasks.signature import try_get_signature

from . import config, todieutri
from .tabbed_listframe import TabbedListFrame

from cch_his_auto_lib.driver import Driver, start_driver
from cch_his_auto_lib.task import auth
from cch_his_auto_lib.action.todieutri.bot_ingiayto import (
    sign_todieutri,
    sign_phieuchidinh,
    sign_phieuthuchienylenh_bn,
    sign_phieuthuchienylenh_bs,
    sign_phieuthuchienylenh_dd,
)
from cch_his_auto_lib.action.chitietnguoibenhnoitru import (
    top_hosobenhan,
)
from cch_his_auto_lib.action.chitietnguoibenhnoitru.top_hosobenhan.tab_hosokhamchuabenh.helper import (
    filter_check_expand_sign,
    goto_row_then_tabdo,
)
from cch_his_auto_lib.action.editor import sign_staff


TITLE = "Khám bệnh mỗi ngày"


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

        nb = ttk.Notebook(self)
        nb.grid(row=1, column=0, sticky="NSEW")

        todieutri_frame = TabbedListFrame(
            nb,
            title="Tờ điều trị",
            item_type=todieutri.Line,
            stats=todieutri.HEADERS_STATS,
        )

        for i, t in enumerate([todieutri_frame]):
            nb.add(t, text=t.get_title_with_count(), sticky="NSEW")

        button_frame = ButtonFrame(self)
        button_frame.grid(row=0, column=1, rowspan=2, padx=20, sticky="S", pady=(0, 20))

        def load():
            cfg = config.load()

            bacsi.set_username(cfg["bacsi"]["username"])
            bacsi.set_password(cfg["bacsi"]["password"])
            dieuduong.set_username(cfg["dieuduong"]["username"])
            dieuduong.set_password(cfg["dieuduong"]["password"])
            dept_var.set(cfg["department"])

            todieutri_frame.clear()
            for item in cfg["todieutri"]:
                todieutri_frame.add_item(item)

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
                "todieutri": todieutri_frame.get_items(),
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
    if not config.is_patient_list_valid(cfg):
        messagebox.showerror(message="Sai data đầu vào")
        return

    with start_driver(headless=run_cfg["headless"], profile_path=PROFILE_PATH) as d:
        if config.is_valid(cfg, "bacsi"):
            with auth.session(
                d,
                cfg["bacsi"]["username"],
                cfg["bacsi"]["password"],
                cfg["department"],
            ):
                run_bs(d, cfg)

        if any(any(p["ky_3tra"]["dieuduong"]) for p in cfg["todieutri"]):
            if config.is_valid(cfg, "dieuduong"):
                with auth.session(
                    d,
                    cfg["dieuduong"]["username"],
                    cfg["dieuduong"]["password"],
                    cfg["department"],
                ):
                    run_dd(d, cfg)

        if any(any(p["ky_3tra"]["benhnhan"]) for p in cfg["todieutri"]):
            for user in get_args(Literal["bacsi", "dieuduong"]):
                if config.is_valid(cfg, user):
                    with auth.session(
                        d,
                        cfg[user]["username"],
                        cfg[user]["password"],
                        cfg["department"],
                    ):
                        run_bn(d, cfg)
                    break
    messagebox.showinfo(message="finish")


def run_bs(d: Driver, cfg: config.Config):
    today = dt.date.today()

    _lgr.info("~~~~~ TỜ ĐIỀU TRỊ ~~~~~")
    for tdt in cfg["todieutri"]:
        d.goto(tdt["url"])
        _log_patient_name(d.waiting(".name span").text)

        if tdt["ky_xn"]:
            sign_phieuchidinh(d)
        if tdt["ky_todieutri"]:
            sign_todieutri(d)
        if any(tdt["ky_3tra"]["bacsi"]):
            sign_phieuthuchienylenh_bs(d, tdt["ky_3tra"]["bacsi"])
        if any([tdt["ky_ct"], tdt["ky_mri"]]):
            with top_hosobenhan.session(d):
                if tdt["ky_ct"]:
                    filter_check_expand_sign(
                        d,
                        name="Phiếu chỉ định chụp cắt lớp vi tính (CT)",
                        chuaky_fn=lambda d, i: goto_row_then_tabdo(
                            d, i, sign_staff.phieuCT_bschidinh
                        ),
                        date=today,
                    )
                if tdt["ky_mri"]:
                    filter_check_expand_sign(
                        d,
                        name="Phiếu chỉ định chụp cộng hưởng từ (MRI)",
                        chuaky_fn=lambda d, i: goto_row_then_tabdo(
                            d, i, sign_staff.phieuMRI_bschidinh
                        ),
                        date=today,
                    )


def run_dd(d: Driver, cfg: config.Config):
    for p in cfg["todieutri"]:
        if any(p["ky_3tra"]["dieuduong"]):
            d.goto(p["url"])
            _log_patient_name(d.waiting(".name span").text)
            sign_phieuthuchienylenh_dd(d, p["ky_3tra"]["dieuduong"])


def run_bn(d: Driver, cfg: config.Config):
    with create_connection() as con:
        for p in cfg["todieutri"]:
            d.goto(p["url"])
            _log_patient_name(d.waiting(".name span").text)
            ma_hs = int(
                d.waiting(
                    ".patient-information .additional-item:nth-child(2) .info",
                    "ma ho so",
                ).text
            )
            if signature := try_get_signature(d, con, ma_hs):
                if any(p["ky_3tra"]["benhnhan"]):
                    sign_phieuthuchienylenh_bn(d, p["ky_3tra"]["benhnhan"], signature)


def _log_patient_name(name: str):
    _lgr.info(
        "\n".join(
            [
                "",
                "~" * 50,
                f"patient: {name}",
                "~" * 50,
            ]
        )
    )
