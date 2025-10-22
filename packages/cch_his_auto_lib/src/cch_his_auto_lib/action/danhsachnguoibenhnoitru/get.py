from cch_his_auto_lib.driver import Driver
from selenium.common import NoSuchElementException


def khoalamviec(d: Driver) -> str:
    return d.waiting(".khoaLamViec div span", "khoa lam viec").text.strip()


def has_next_page(d: Driver) -> bool:
    try:
        d.waiting(".ant-pagination-next:not(.ant-pagination-disabled)")
        return True
    except NoSuchElementException:
        return False
