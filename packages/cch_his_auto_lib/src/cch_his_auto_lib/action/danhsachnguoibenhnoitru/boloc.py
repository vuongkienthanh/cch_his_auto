from contextlib import contextmanager
import datetime as dt

from cch_his_auto_lib.driver import Driver

BOLOC_POPOVER = ".ant-popover:has(form +div button)"


@contextmanager
def open_menu(d: Driver):
    d.clicking("#base-search_component .ant-col:nth-child(1) button", "Bộ lọc button")
    d.waiting(BOLOC_POPOVER)
    try:
        yield
    finally:
        d.clicking(f"{BOLOC_POPOVER} form +div button", "Tìm button")
        d.wait_closing(BOLOC_POPOVER)


def send(
    d: Driver,
    vaokhoa: tuple[dt.date, dt.date] | None = None,
    nhapvien: tuple[dt.date, dt.date] | None = None,
    ravien: tuple[dt.date, dt.date] | None = None,
):
    """
    send info to menu bộ lọc
    """
    if not any([vaokhoa, nhapvien, ravien]):
        return
    fmt = "%Y-%m-%d"

    for loc, date in zip([8, 11, 14], [vaokhoa, nhapvien, ravien]):
        if date is None:
            continue
        start_d = date[0].strftime(fmt)
        end_d = date[1].strftime(fmt)
        d.clear_input(
            f"{BOLOC_POPOVER} form .ant-form-item.date-1:nth-child({loc}) .ant-picker-input:nth-child(1) input"
        ).send_keys(start_d)
        d.clear_input(
            f"{BOLOC_POPOVER} form .ant-form-item.date-1:nth-child({loc}) .ant-picker-input:nth-child(3) input"
        ).send_keys(end_d)
