import time
from enum import StrEnum

from selenium.common import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver import ActionChains, Keys

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.tracing import EndOfLoop
from . import _lgr, _trace


class _State(StrEnum):
    Register = "Đăng ký PHCN"
    AddNew = "Thêm mới đợt PHCN"
    Cancel = "Hủy đăng ký PHCN"


def _open():
    _d = get_global_driver()
    _d.clicking(".footer-btn .left button:nth-child(3)", f"{_State.Register} button")
    _d.waiting(".ant-form", "PHCN dialog")


def _cancel():
    _d = get_global_driver()
    _d.clicking(".footer-btn .left button:nth-child(3)", f"{_State.Cancel} button")
    _d.waiting_to_startswith(
        ".footer-btn .left button:nth-child(3)",
        _State.AddNew,
        f"{_State.Cancel} becomes {_State.AddNew}",
    )


@_trace
def open_dialog():
    "Click *Đăng ký PHCN* or *Thêm mới đợt PHCN* button"
    _d = get_global_driver()
    for i in range(120):
        time.sleep(1)
        try:
            _lgr.debug(f"checking PHCN button state {i}...")
            ele = _d.waiting(".footer-btn .left button:nth-child(3)", "PHCN button")
            if ele.text.strip() == _State.Register:
                _lgr.debug(f"PHCN button state is {_State.Register}")
                _open()
                return
            elif ele.text.strip() == _State.AddNew:
                _lgr.debug(f"PHCN button state is {_State.AddNew}")
                _open()
                return
            elif ele.text.strip() == _State.Cancel:
                _lgr.debug(f"PHCN button state is {_State.Cancel}")
                _cancel()
                _open()
                return
        except StaleElementReferenceException as e:
            _lgr.warning(f"get {e}")
    else:
        raise EndOfLoop("can't open PHCN dialog")


@_trace
def cancel():
    "Click *Hủy đăng ký PHCN* button"
    _d = get_global_driver()
    for i in range(120):
        time.sleep(1)
        try:
            _lgr.debug(f"checking PHCN button state {i}...")
            ele = _d.waiting(".footer-btn .left button:nth-child(3)", "PHCN button")
            if ele.text.strip() == _State.Register:
                raise Exception(f"Button state is {_State.Register}")
            elif ele.text.strip() == _State.AddNew:
                raise Exception(f"Button state is {_State.AddNew}")
            elif ele.text.strip() == _State.Cancel:
                _lgr.debug(f"PHCN button state is {_State.Cancel}")
                _cancel()
                return
        except StaleElementReferenceException as e:
            _lgr.warning(f"get {e}")
    else:
        raise EndOfLoop("can't cancel PHCN")


@_trace
def clear():
    "After `open_dialog`, clear all selections"
    _d = get_global_driver()
    for ele in _d.find_all(".ant-form .ant-select-selection-item-remove"):
        _lgr.debug(f"removing {ele.text}")
        ele.click()


@_trace
def drop_menu():
    "After `open_dialog`, drop down the menu"
    _d = get_global_driver()
    _d.waiting(".ant-form .ant-select", "drop menu PHCN").send_keys(Keys.DOWN)


@_trace
def close_menu():
    "After `dropmenu`, close the menu"
    _d = get_global_driver()
    ActionChains(_d).send_keys(Keys.ESCAPE).perform()


@_trace
def add_bunuot():
    "After `drop_menu`, Add *bú nuốt*"
    _d = get_global_driver()
    _d.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(2)", "add Bú nuốt"
    )


@_trace
def add_giaotiep():
    "After `drop_menu`, Add *giao tiếp*"
    _d = get_global_driver()
    _d.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(3)", "add Giao tiếp"
    )


@_trace
def add_hohap():
    "After `drop_menu`, Add *hô hấp*"
    _d = get_global_driver()
    _d.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(4)", "add Hô hấp"
    )


@_trace
def add_vandong():
    "After `drop_menu`, Add *vận động*"
    _d = get_global_driver()
    _d.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(5)", "add Vận động"
    )


@_trace
def save():
    "Finish and click save dialog"
    _d = get_global_driver()
    _d.clicking(".ant-modal-body .bottom-action-right button", "save button")
    for i in range(120):
        time.sleep(1)
        try:
            _lgr.debug(f"checking PHCN button state {i}...")
            ele = _d.find(".footer-btn .left button:nth-child(3)")
            if ele.text.strip() == _State.Cancel:
                _lgr.debug(f"PHCN button state is {_State.Cancel}")
                return
        except (StaleElementReferenceException, NoSuchElementException) as e:
            _lgr.warning(f"get {e}")
    else:
        raise EndOfLoop("can't save PHCN dialog")
