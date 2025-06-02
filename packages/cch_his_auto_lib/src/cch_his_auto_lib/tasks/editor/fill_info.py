from selenium.webdriver import ActionChains, Keys
from cch_his_auto_lib.driver import get_global_driver


def check_than_click(css):
    _d = get_global_driver()
    if _d.waiting(f"{css} span").text.strip() == "":
        _d.clicking(css)


def bienbanhoichan_fill_info(khac: str):
    _d = get_global_driver()
    # _d.clear_input(
    #     ".layout-line-item .layout-line-item:nth-child(37) span[contenteditable]"
    # ).send_keys(khac)
    ActionChains(_d).click(
        _d.find(
            ".layout-line-item .layout-line-item:nth-child(37) span[contenteditable]"
        )
    ).send_keys(Keys.CONTROL, "a").send_keys(Keys.DELETE).send_keys(khac).perform()


def phieudutrucungcapmau_fill_info(
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
    _d = get_global_driver()

    duphongphauthuat_css = ".layout-line-item:nth-child(7)>div:nth-child(2) .check-item:nth-child(1) .check-box-contain"
    nhom1_css = ".layout-line-item:nth-child(7)>div:nth-child(2) .check-item:nth-child(2) .check-box-contain"
    nhom2_css = ".layout-line-item:nth-child(7)>div:nth-child(2) .check-item:nth-child(3) .check-box-contain"
    if duphongphauthuat:
        check_than_click(duphongphauthuat_css)
        if nhom1:
            check_than_click(nhom1_css)
        else:
            check_than_click(nhom2_css)
        _d.clicking(".layout-line-item:nth-child(7)>div:nth-child(4) .value-display")
        _d.clear_input(
            ".layout-line-item:nth-child(7)>div:nth-child(4) input"
        ).send_keys(date)

    yes = ".layout-line-item:nth-child(13)>div:nth-child(2) .check-item:nth-child(1) .check-box-contain"
    no = ".layout-line-item:nth-child(13)>div:nth-child(2) .check-item:nth-child(2) .check-box-contain"
    if datruyenmau:
        check_than_click(yes)
    else:
        check_than_click(no)

    yes = ".layout-line-item:nth-child(13)>div:nth-child(3) .check-item:nth-child(1) .check-box-contain"
    no = ".layout-line-item:nth-child(13)>div:nth-child(3) .check-item:nth-child(2) .check-box-contain"
    if khangthebatthuong:
        check_than_click(yes)
    else:
        check_than_click(no)

    yes = ".layout-line-item:nth-child(14)>div:nth-child(4) .check-item:nth-child(1) .check-box-contain"
    no = ".layout-line-item:nth-child(14)>div:nth-child(4) .check-item:nth-child(2) .check-box-contain"
    if phanungtruyenmau:
        check_than_click(yes)
    else:
        check_than_click(no)

    _d.clear_input(
        ".layout-line-item:nth-child(15)>div:nth-child(2) [contenteditable]"
    ).send_keys(hcthientai)

    yes = ".layout-line-item:nth-child(16) .check-item:nth-child(1) .check-box-contain"
    no = ".layout-line-item:nth-child(16) .check-item:nth-child(2) .check-box-contain"
    if truyenmaucochieuxa:
        check_than_click(yes)
    else:
        check_than_click(no)

    yes = ".layout-line-item:nth-child(17) .check-item:nth-child(1) .check-box-contain"
    no = ".layout-line-item:nth-child(17) .check-item:nth-child(2) .check-box-contain"
    if cungnhom:
        check_than_click(yes)
    else:
        check_than_click(no)


def phieucamkettruyenmau_fill_info():
    check_than_click(
        ".component-page .layout-line-item:nth-child(10) .check-item:first-child .check-box-contain"
    )


def phieucamkettta5_fill_info():
    check_than_click(
        ".component-page .layout-line-item:nth-child(10) .check-item:first-child .check-box-contain"
    )
