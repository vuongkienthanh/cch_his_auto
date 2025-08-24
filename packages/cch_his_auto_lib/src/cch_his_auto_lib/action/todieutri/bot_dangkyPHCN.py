import time
from enum import StrEnum

from selenium.common import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver import ActionChains, Keys

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.errors import EndOfLoopException
from . import _lgr, _trace


class _State(StrEnum):
    Register = "Đăng ký PHCN"
    AddNew = "Thêm mới đợt PHCN"
    Cancel = "Hủy đăng ký PHCN"


def _open(d: Driver):
    d.clicking(".footer-btn .left button:nth-child(3)", f"{_State.Register} button")
    d.waiting(".ant-form", "PHCN dialog")


def _cancel(d: Driver):
    d.clicking(".footer-btn .left button:nth-child(3)", f"{_State.Cancel} button")
    d.waiting_to_startswith(
        ".footer-btn .left button:nth-child(3)",
        _State.AddNew,
        f"{_State.Cancel} becomes {_State.AddNew}",
    )


@_trace
def open_dialog(d: Driver):
    "Click *Đăng ký PHCN* or *Thêm mới đợt PHCN* button"
    for i in range(120):
        time.sleep(1)
        try:
            _lgr.debug(f"checking PHCN button state {i}...")
            ele = d.waiting(".footer-btn .left button:nth-child(3)", "PHCN button")
            if ele.text.strip() == _State.Register:
                _lgr.debug(f"PHCN button state is {_State.Register}")
                _open(d)
                return
            elif ele.text.strip() == _State.AddNew:
                _lgr.debug(f"PHCN button state is {_State.AddNew}")
                _open(d)
                return
            elif ele.text.strip() == _State.Cancel:
                _lgr.debug(f"PHCN button state is {_State.Cancel}")
                _cancel(d)
                _open(d)
                return
        except StaleElementReferenceException as e:
            _lgr.warning(f"get {e}")
    else:
        raise EndOfLoopException("can't open PHCN dialog")


def cancel(d: Driver):
    "Click *Hủy đăng ký PHCN* button"
    for i in range(120):
        time.sleep(1)
        try:
            _lgr.debug(f"checking PHCN button state {i}...")
            ele = d.waiting(".footer-btn .left button:nth-child(3)", "PHCN button")
            if ele.text.strip() == _State.Register:
                raise Exception(f"Button state is {_State.Register}")
            elif ele.text.strip() == _State.AddNew:
                raise Exception(f"Button state is {_State.AddNew}")
            elif ele.text.strip() == _State.Cancel:
                _lgr.debug(f"PHCN button state is {_State.Cancel}")
                _cancel(d)
                return
        except StaleElementReferenceException as e:
            _lgr.warning(f"get {e}")
    else:
        raise EndOfLoopException("can't cancel PHCN")


def clear(d: Driver):
    "After `open_dialog`, clear all selections"
    for ele in d.find_all(".ant-form .ant-select-selection-item-remove"):
        _lgr.debug(f"removing {ele.text}")
        ele.click()


def drop_menu(d: Driver):
    "After `open_dialog`, drop down the menu"
    d.waiting(".ant-form .ant-select", "drop menu PHCN").send_keys(Keys.DOWN)


def close_menu(d: Driver):
    "After `dropmenu`, close the menu"
    ActionChains(d).send_keys(Keys.ESCAPE).perform()


def add_bunuot(d: Driver):
    "After `drop_menu`, Add *bú nuốt*"
    d.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(2)", "add Bú nuốt"
    )


def add_giaotiep(d: Driver):
    "After `drop_menu`, Add *giao tiếp*"
    d.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(3)", "add Giao tiếp"
    )


def add_hohap(d: Driver):
    "After `drop_menu`, Add *hô hấp*"
    d.clicking(".rc-virtual-list div.ant-select-item-option:nth-child(4)", "add Hô hấp")


def add_vandong(d: Driver):
    "After `drop_menu`, Add *vận động*"
    d.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(5)", "add Vận động"
    )


@_trace
def save(d: Driver):
    "Finish and click save dialog"
    d.clicking(".ant-modal-body .bottom-action-right button", "save button")
    for i in range(120):
        time.sleep(1)
        try:
            _lgr.debug(f"checking PHCN button state {i}...")
            ele = d.find(".footer-btn .left button:nth-child(3)")
            if ele.text.strip() == _State.Cancel:
                _lgr.debug(f"PHCN button state is {_State.Cancel}")
                return
        except (StaleElementReferenceException, NoSuchElementException) as e:
            _lgr.warning(f"get {e}")
    else:
        raise EndOfLoopException("can't save PHCN dialog")
