import time

from cch_his_auto_lib.driver import Driver


def huytimkiem(d: Driver):
    d.clicking(
        "#base-search_component > div > div:nth-child(2) button:first-child",
        "Hủy tìm kiếm",
    )
    time.sleep(5)  # no change on UI


def next_page(d: Driver):
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
