from selenium.common import NoSuchElementException
from cch_his_auto_lib.driver import Driver


def wait_loaded(d: Driver):
    try:
        d.waiting(".app-main")
    except NoSuchElementException:
        d.refresh()
        d.waiting(".app-main")


def check_than_click(d: Driver, css):
    "for check box with css .check-item, make sure it is checked"
    if d.waiting(f"{css} .check-box-contain span").text.strip() == "":
        d.clicking(css)
