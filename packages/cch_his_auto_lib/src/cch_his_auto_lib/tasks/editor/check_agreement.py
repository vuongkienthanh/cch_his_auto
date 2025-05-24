from cch_his_auto_lib.driver import get_global_driver


def phieucamkettruyenmau() -> bool:
    _d = get_global_driver()
    return (
        _d.waiting(
            ".component-page .layout-line-item:nth-child(10) .check-item:first-child .check-box-contain",
            "agree checkbox",
        ).text.strip()
        == "x"
    )


def check_phieucamkettruyenmau():
    _d = get_global_driver()
    if not phieucamkettruyenmau():
        _d.clicking(
            ".component-page .layout-line-item:nth-child(10) .check-item:first-child .check-box-contain",
            "agree checkbox",
        )


def phieucamkettta5() -> bool:
    _d = get_global_driver()
    return (
        _d.waiting(
            ".component-page .layout-line-item:nth-child(10) .check-item:first-child .check-box-contain",
            "agree checkbox",
        ).text.strip()
        == "x"
    )


def check_phieucamkettta5():
    _d = get_global_driver()
    if not phieucamkettta5():
        _d.clicking(
            ".component-page .layout-line-item:nth-child(10) .check-item:first-child .check-box-contain",
            "agree checkbox",
        )
