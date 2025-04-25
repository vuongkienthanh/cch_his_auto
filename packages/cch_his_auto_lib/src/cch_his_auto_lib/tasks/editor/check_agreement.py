from cch_his_auto_lib.driver import Driver


def phieucamkettruyenmau(driver: Driver) -> bool:
    return (
        driver.waiting(
            ".component-page .layout-line-item:nth-child(10) .check-item:first-child .check-box-contain",
            "agree checkbox",
        ).text.strip()
        == "x"
    )


def check_phieucamkettruyenmau(driver: Driver):
    if not phieucamkettruyenmau(driver):
        driver.clicking(
            ".component-page .layout-line-item:nth-child(10) .check-item:first-child .check-box-contain",
            "agree checkbox",
        )


def phieucamkettta5(driver: Driver) -> bool:
    return (
        driver.waiting(
            ".component-page .layout-line-item:nth-child(10) .check-item:first-child .check-box-contain",
            "agree checkbox",
        ).text.strip()
        == "x"
    )


def check_phieucamkettta5(driver: Driver):
    if not phieucamkettta5(driver):
        driver.clicking(
            ".component-page .layout-line-item:nth-child(10) .check-item:first-child .check-box-contain",
            "agree checkbox",
        )
