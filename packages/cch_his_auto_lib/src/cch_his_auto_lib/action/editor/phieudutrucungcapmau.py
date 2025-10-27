from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import console
from . import wait_loaded, check_than_click


def fill_info(
    d: Driver,
    duphongphauthuat: bool,
    nhom1: bool,
    date: str,
    datruyenmau: bool,
    khangthebatthuong: bool,
    phanungtruyenmau: bool,
    hcthientai: str,
    truyenmaucochieuxa: bool,
    cungnhom: bool,
):
    wait_loaded(d)

    duphongphauthuat_css = (
        ".layout-line-item:nth-child(7)>div:nth-child(2) .check-item:nth-child(1)"
    )
    nhom1_css = (
        ".layout-line-item:nth-child(7)>div:nth-child(2) .check-item:nth-child(2)"
    )
    nhom2_css = (
        ".layout-line-item:nth-child(7)>div:nth-child(2) .check-item:nth-child(3)"
    )
    if duphongphauthuat:
        check_than_click(d, duphongphauthuat_css)
        if nhom1:
            check_than_click(d, nhom1_css)
        else:
            check_than_click(d, nhom2_css)
        d.clicking(".layout-line-item:nth-child(7)>div:nth-child(4) .value-display")
        d.clear_input(
            ".layout-line-item:nth-child(7)>div:nth-child(4) input"
        ).send_keys(date)

    yes = ".layout-line-item:nth-child(13)>div:nth-child(2) .check-item:nth-child(1)"
    no = ".layout-line-item:nth-child(13)>div:nth-child(2) .check-item:nth-child(2)"
    if datruyenmau:
        check_than_click(d, yes)
    else:
        check_than_click(d, no)

    yes = ".layout-line-item:nth-child(13)>div:nth-child(3) .check-item:nth-child(1)"
    no = ".layout-line-item:nth-child(13)>div:nth-child(3) .check-item:nth-child(2)"
    if khangthebatthuong:
        check_than_click(d, yes)
    else:
        check_than_click(d, no)

    yes = ".layout-line-item:nth-child(14)>div:nth-child(4) .check-item:nth-child(1)"
    no = ".layout-line-item:nth-child(14)>div:nth-child(4) .check-item:nth-child(2)"
    if phanungtruyenmau:
        check_than_click(d, yes)
    else:
        check_than_click(d, no)

    d.clear_input(
        ".layout-line-item:nth-child(15)>div:nth-child(2) [contenteditable]"
    ).send_keys(hcthientai)

    yes = ".layout-line-item:nth-child(16) .check-item:nth-child(1)"
    no = ".layout-line-item:nth-child(16) .check-item:nth-child(2)"
    if truyenmaucochieuxa:
        check_than_click(d, yes)
    else:
        check_than_click(d, no)

    yes = ".layout-line-item:nth-child(17) .check-item:nth-child(1)"
    no = ".layout-line-item:nth-child(17) .check-item:nth-child(2)"
    if cungnhom:
        check_than_click(d, yes)
    else:
        check_than_click(d, no)


def bs(d: Driver):
    with console.status("signing phiếu dự trù cung cấp máu..."):
        wait_loaded(d)
        d.sign_staff_signature(
            btn_css=".sign-image button",
            btn_txt="Xác nhận ký BÁC SĨ ĐIỀU TRỊ",
            img_css=".sign-image img",
            name="phieu du tru cung cap mau",
        )
