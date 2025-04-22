from contextlib import contextmanager

from cch_his_auto.driver import Driver

DIALOG_CSS = ".ant-modal:has(.ant-row:first-child+.more-info)"


@contextmanager
def session(driver: Driver):
    open_dialog(driver)
    try:
        yield
    finally:
        save(driver)


def open_dialog(driver: Driver):
    driver.clicking_svg(
        ".tab-box .info:nth-child(3) .title svg", "edit thongtinravien button"
    )
    driver.waiting(DIALOG_CSS, "edit thongtinravien dialog")


def save(driver: Driver):
    driver.clicking(
        f"{DIALOG_CSS} .bottom-action-right button:nth-child(2)",
        "save button",
    )
    driver.wait_closing(DIALOG_CSS, "edit thongtinra vien dialog")


def set_discharge_diagnosis_detail(driver: Driver, value: str):
    driver.clear_input(
        f"{DIALOG_CSS} .ant-row .ant-col:nth-child(1)>div:nth-child(3) textarea"
    ).send_keys(value)
