import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import TimeoutException, NoSuchElementException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import _root_lgr, console

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


def load_and_clear(d: Driver):
    with console.status("load danh sách người bệnh nội trú -> hủy tìm kiếm"):
        d.get(URL)
        wait_loaded(d)
        click_huytimkiem(d)


def load(d: Driver):
    d.goto(URL)
    wait_loaded(d)


def get_khoalamviec(d: Driver) -> str:
    return d.waiting(".khoaLamViec div span", "khoa lam viec").text.strip()


def has_next_page(d: Driver) -> bool:
    try:
        d.waiting(".ant-pagination-next:not(.ant-pagination-disabled)")
        return True
    except NoSuchElementException:
        return False


def click_huytimkiem(d: Driver):
    d.clicking(
        "#base-search_component > div > div:nth-child(2) button:first-child",
        "Hủy tìm kiếm",
    )
    time.sleep(5)  # no change on UI


def click_next_page(d: Driver):
    current_page = d.waiting(
        ".ant-pagination.patient-paging li.ant-pagination-item-active"
    ).get_attribute("title")
    assert current_page is not None
    next_page = int(current_page) + 1
    d.clicking(".ant-pagination-next:not(.ant-pagination-disabled) button")
    d.waiting(
        f".ant-pagination.patient-paging li.ant-pagination-item-active[title='{next_page}']"
    )
    time.sleep(5)
