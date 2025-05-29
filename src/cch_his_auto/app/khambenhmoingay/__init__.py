import tkinter as tk
from tkinter import messagebox, ttk
import datetime as dt
from typing import Literal, get_args
from functools import partial

from cch_his_auto.app import PROFILE_PATH, _lgr
from cch_his_auto.global_db import create_connection
from cch_his_auto.common_ui.staff_info import UsernamePasswordFrame
from cch_his_auto.common_ui.button_frame import ButtonFrame, RunConfig, setLogLevel
from cch_his_auto.common_tasks.signature import try_get_signature

from . import config, todieutri, dutrumau, bbhc

from cch_his_auto_lib.driver import start_global_driver, get_global_driver
from cch_his_auto_lib.tasks import auth
from cch_his_auto_lib.tasks.todieutri.bot_ingiayto import (
    sign_todieutri,
    sign_phieuchidinh,
    sign_phieuthuchienylenh_bn,
    sign_phieuthuchienylenh_bs,
    sign_phieuthuchienylenh_dd,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import (
    top_hosobenhan,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.top_hosobenhan.tab_hosokhamchuabenh.helper import (
    filter_check_expand_sign,
    goto_row_then_tabdo,
)
from cch_his_auto_lib.tasks.editor import sign_staff_name


TITLE = "Khám bệnh mỗi ngày"


class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        info = tk.LabelFrame(self, text="Thông tin đăng nhập")
        bacsi = UsernamePasswordFrame(info, text="Bác sĩ")
        dieuduong = UsernamePasswordFrame(info, text="Điều dưỡng")
        truongkhoa = UsernamePasswordFrame(info, text="Trưởng khoa")
        bacsi.grid(row=0, column=0)
        dieuduong.grid(row=0, column=1)
        truongkhoa.grid(row=0, column=2)
        dept_var = tk.StringVar()
        tk.Label(info, text="Khoa lâm sàng:", justify="right").grid(
            row=1, column=0, sticky="E"
        )
        tk.Entry(info, textvariable=dept_var).grid(row=1, column=1, sticky="W")
        info.grid(row=0, column=0, sticky="N", pady=20)

        nb = ttk.Notebook(self, name="kcb_notebook")
        nb.grid(row=1, column=0, sticky="NSEW")

        todieutri_frame = todieutri.Frame(self)
        dutrumau_frame = dutrumau.Frame(self)
        bbhc_frame = bbhc.Frame(self)

        for i, t in enumerate([todieutri_frame, dutrumau_frame, bbhc_frame]):
            t.set_tab_index(i)
            nb.add(t, text=t.get_title(), sticky="NSEW")

        button_frame = ButtonFrame(self)
        button_frame.grid(row=0, column=1, rowspan=2, padx=20, sticky="S", pady=(0, 20))

        def load():
            cfg = config.load()

            for w, name in zip(
                [bacsi, dieuduong, truongkhoa],  # widgets
                ["bacsi", "dieuduong", "truongkhoa"],  # dict names
            ):
                w.set_username(cfg[name]["username"])
                w.set_password(cfg[name]["password"])

            dept_var.set(cfg["department"])

            for w, name in zip(
                [todieutri_frame, dutrumau_frame, bbhc_frame],
                ["todieutri", "dutrumau", "bbhc"],
            ):
                w.clear()
                for p in cfg[name]:
                    w.add_item(p)

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
                "truongkhoa": {
                    "username": dieuduong.get_username(),
                    "password": dieuduong.get_password(),
                },
                "department": dept_var.get(),
                "todieutri": todieutri_frame.get_items(),
                "dutrumau": dutrumau_frame.get_items(),
                "bbhc": bbhc_frame.get_items(),
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

    setLogLevel(run_cfg)
    with start_global_driver(headless=run_cfg["headless"], profile_path=PROFILE_PATH):
        if config.is_valid(cfg, "bacsi"):
            with auth.session(
                cfg["bacsi"]["username"],
                cfg["bacsi"]["password"],
                cfg["department"],
            ):
                run_bs(cfg)

        if any(p["ky_3tra"]["dieuduong"] for p in cfg["todieutri"]):
            if config.is_valid(cfg, "dieuduong"):
                with auth.session(
                    cfg["dieuduong"]["username"],
                    cfg["dieuduong"]["password"],
                    cfg["department"],
                ):
                    run_dd(cfg)

        if any(p["ky_3tra"]["benhnhan"] for p in cfg["todieutri"]):
            for user in get_args(Literal["bacsi", "dieuduong"]):
                if config.is_valid(cfg, user):
                    with auth.session(
                        cfg[user]["username"],
                        cfg[user]["password"],
                        cfg["department"],
                    ):
                        run_bn(cfg)
                    break
        if any(cfg["bbhc"]):
            if config.is_valid(cfg, "truongkhoa"):
                run_tk(cfg)
    messagebox.showinfo(message="finish")


def run_bs(cfg: config.Config):
    driver = get_global_driver()
    d = dt.date.today()

    _lgr.info("~~~~~ TỜ ĐIỀU TRỊ ~~~~~")
    for tdt in cfg["todieutri"]:
        driver.goto(tdt["url"])
        log_patient_name(driver.waiting(".name span").text)

        if tdt["ky_xn"]:
            sign_phieuchidinh()
        if tdt["ky_todieutri"]:
            sign_todieutri()
        if any(tdt["ky_3tra"]["bacsi"]):
            sign_phieuthuchienylenh_bs(tdt["ky_3tra"]["bacsi"])
        if any([tdt["ky_ct"], tdt["ky_mri"]]):
            with top_hosobenhan.session():
                if tdt["ky_ct"]:
                    filter_check_expand_sign(
                        name="Phiếu chỉ định chụp cắt lớp vi tính (CT)",
                        chuaky_fn=lambda i: goto_row_then_tabdo(
                            i, sign_staff_name.phieuCT_bschidinh
                        ),
                        date=d,
                    )
                if tdt["ky_mri"]:
                    filter_check_expand_sign(
                        name="Phiếu chỉ định chụp cộng hưởng từ (MRI)",
                        chuaky_fn=lambda i: goto_row_then_tabdo(
                            i, sign_staff_name.phieuMRI_bschidinh
                        ),
                        date=d,
                    )
    _lgr.info("~~~~~ DỰ TRÙ MÁU ~~~~~")
    for dtm in cfg["dutrumau"]:
        driver.goto(dtm["url"])
        log_patient_name(driver.waiting(".name span").text)
        with top_hosobenhan.session():
            filter_check_expand_sign(
                "Phiếu dự trù và cung cấp máu",
                chuaky_fn=lambda i: goto_row_then_tabdo(
                    i,
                    partial(
                        sign_staff_name.phieudutrucungcapmau_fill_info_then_sign,
                        dtm["duphongphauthuat"],
                        dtm["nhom1"],
                        dtm["date"],
                        dtm["datruyenmau"],
                        dtm["khangthebatthuong"],
                        dtm["phanungtruyenmau"],
                        dtm["hcthientai"],
                        dtm["truyenmaucochieuxa"],
                        dtm["cungnhom"],
                    ),
                ),
            )

    _lgr.info("~~~~~ BIÊN BẢN HỘI CHẨN ~~~~~")
    for bbhc in cfg["bbhc"]:
        driver.goto(bbhc["url"])
        log_patient_name(driver.waiting(".name span").text)
        with top_hosobenhan.session():
            filter_check_expand_sign(
                "Biên bản hội chẩn",
                chuaky_fn=lambda i: goto_row_then_tabdo(
                    i,
                    partial(
                        sign_staff_name.bienbanhoichan_fill_info_then_thuky,
                        bbhc["khac"],
                    ),
                ),
                date=d,
            )


def run_dd(cfg: config.Config):
    driver = get_global_driver()
    for p in cfg["todieutri"]:
        if any(p["ky_3tra"]["dieuduong"]):
            driver.goto(p["url"])
            log_patient_name(driver.waiting(".name span").text)
            sign_phieuthuchienylenh_dd(p["ky_3tra"]["dieuduong"])


def run_bn(cfg: config.Config):
    driver = get_global_driver()
    with create_connection() as con:
        for p in cfg["todieutri"]:
            driver.goto(p["url"])
            log_patient_name(driver.waiting(".name span").text)
            ma_hs = int(
                driver.waiting(
                    ".patient-information .additional-item:nth-child(2) .info",
                    "ma ho so",
                ).text
            )
            if signature := try_get_signature(con, ma_hs):
                if any(p["ky_3tra"]["benhnhan"]):
                    sign_phieuthuchienylenh_bn(p["ky_3tra"]["benhnhan"], signature)


def run_tk(cfg: config.Config):
    driver = get_global_driver()
    d = dt.date.today()
    for bbhc in cfg["bbhc"]:
        driver.goto(bbhc["url"])
        log_patient_name(driver.waiting(".name span").text)
        with top_hosobenhan.session():
            filter_check_expand_sign(
                "Biên bản hội chẩn",
                chuaky_fn=lambda i: goto_row_then_tabdo(
                    i,
                    sign_staff_name.bienbanhoichan_truongkhoa,
                ),
                date=d,
            )


def log_patient_name(name: str):
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
