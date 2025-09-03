from cch_his_auto_lib.driver import Driver


def check_than_click(d: Driver, css):
    if d.waiting(f"{css} span").text.strip() == "":
        d.clicking(css)


def phieudutrucungcapmau_fill_info(
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
    duphongphauthuat_css = ".layout-line-item:nth-child(7)>div:nth-child(2) .check-item:nth-child(1) .check-box-contain"
    nhom1_css = ".layout-line-item:nth-child(7)>div:nth-child(2) .check-item:nth-child(2) .check-box-contain"
    nhom2_css = ".layout-line-item:nth-child(7)>div:nth-child(2) .check-item:nth-child(3) .check-box-contain"
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

    yes = ".layout-line-item:nth-child(13)>div:nth-child(2) .check-item:nth-child(1) .check-box-contain"
    no = ".layout-line-item:nth-child(13)>div:nth-child(2) .check-item:nth-child(2) .check-box-contain"
    if datruyenmau:
        check_than_click(d, yes)
    else:
        check_than_click(d, no)

    yes = ".layout-line-item:nth-child(13)>div:nth-child(3) .check-item:nth-child(1) .check-box-contain"
    no = ".layout-line-item:nth-child(13)>div:nth-child(3) .check-item:nth-child(2) .check-box-contain"
    if khangthebatthuong:
        check_than_click(d, yes)
    else:
        check_than_click(d, no)

    yes = ".layout-line-item:nth-child(14)>div:nth-child(4) .check-item:nth-child(1) .check-box-contain"
    no = ".layout-line-item:nth-child(14)>div:nth-child(4) .check-item:nth-child(2) .check-box-contain"
    if phanungtruyenmau:
        check_than_click(d, yes)
    else:
        check_than_click(d, no)

    d.clear_input(
        ".layout-line-item:nth-child(15)>div:nth-child(2) [contenteditable]"
    ).send_keys(hcthientai)

    yes = ".layout-line-item:nth-child(16) .check-item:nth-child(1) .check-box-contain"
    no = ".layout-line-item:nth-child(16) .check-item:nth-child(2) .check-box-contain"
    if truyenmaucochieuxa:
        check_than_click(d, yes)
    else:
        check_than_click(d, no)

    yes = ".layout-line-item:nth-child(17) .check-item:nth-child(1) .check-box-contain"
    no = ".layout-line-item:nth-child(17) .check-item:nth-child(2) .check-box-contain"
    if cungnhom:
        check_than_click(d, yes)
    else:
        check_than_click(d, no)


def phieucamkettruyenmau_fill_info(d: Driver):
    check_than_click(
        d,
        ".component-page .layout-line-item:nth-child(10) .check-item:first-child .check-box-contain",
    )


def phieucamkettta5_fill_info(d: Driver):
    check_than_click(
        d,
        ".component-page .layout-line-item:nth-child(10) .check-item:first-child .check-box-contain",
    )
