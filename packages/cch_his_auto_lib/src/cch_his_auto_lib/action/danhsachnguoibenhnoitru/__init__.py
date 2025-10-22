import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import TimeoutException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import _root_lgr

URL = "http://emr.ndtp.org/quan-ly-noi-tru/danh-sach-nguoi-benh-noi-tru"

_lgr = _root_lgr.getChild("danhsachnguoibenhnoitru")


def wait_loaded(d: Driver):
    try:
        WebDriverWait(d, 120).until(
            lambda _: len(d.find_all(".main__container tr.ant-table-row")) >= 1
        )
    except TimeoutException:
        d.refresh()
        WebDriverWait(d, 120).until(
            lambda _: len(d.find_all(".main__container tr.ant-table-row")) >= 1
        )
    finally:
        time.sleep(5)


def load(d: Driver):
    from .click import huytimkiem

    d.goto(URL)
    wait_loaded(d)
    huytimkiem(d)
