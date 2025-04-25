import datetime as dt

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.helper import EndOfLoop, tracing
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import _logger, ACTIVE_PANE

TAB_NUMBER = 3
_logger = _logger.getChild("tab_todieutri")
_trace = tracing(_logger)


def show_only_khoalamviec(driver: Driver):
    driver.clicking2(f"{ACTIVE_PANE} h1 svg:last-child")
    driver.clicking2(".ant-popover .ant-radio-group label:last-child input")
    driver.clicking2(".ant-popover .ant-radio-group label:first-child input")
    driver.clicking2(f"{ACTIVE_PANE} h1 svg:last-child")


def show_all_khoa(driver: Driver):
    driver.clicking2(f"{ACTIVE_PANE} h1 svg:last-child")
    driver.clicking2(".ant-popover .ant-radio-group label:first-child input")
    driver.clicking2(".ant-popover .ant-radio-group label:last-child input")
    driver.clicking2(f"{ACTIVE_PANE} h1 svg:last-child")


def get_all_ngaydieutri(driver: Driver) -> list[WebElement]:
    "return only date part"
    return driver.find_all(
        f"{ACTIVE_PANE} .ant-collapse-item>.ant-collapse-header .right>span:first-child"
    )


def get_all_todieutri_at_date(driver: Driver, date: dt.date) -> list[WebElement]:
    "return only time part"
    date_str = date.strftime("%d/%m/%Y")
    for i, d in enumerate(get_all_ngaydieutri(driver), 1):
        if d.text.strip()[:10] == date_str:
            return driver.find_all(
                f"{ACTIVE_PANE} .ant-collapse-item:nth-child({i})>.ant-collapse-content .left"
            )
    raise EndOfLoop(f"can't find todieutri at date= {date}")


@_trace
def click_nearest_todieutri_to_datetime(driver: Driver, _dt: dt.datetime):
    def timeval(time: dt.time) -> int:
        return time.hour * 24 + time.minute * 60

    date = _dt.date()
    time = timeval(_dt.time())

    min_ele = min(
        get_all_todieutri_at_date(driver, date),
        key=lambda ele: abs(
            time - timeval(dt.datetime.strptime(ele.text.strip(), "%H:%M:%S").time())
        ),
    )
    ActionChains(driver).click(min_ele).perform()
    driver.waiting(f"{ACTIVE_PANE} .ant-collapse-item .actived")


@_trace
def open_nearest_todieutri_to_datetime(driver: Driver, _dt: dt.datetime):
    click_nearest_todieutri_to_datetime(driver, _dt)
    driver.clicking2(f"{ACTIVE_PANE} .ant-collapse-item .actived .right svg:last-child")
    driver.wait_closing(f"{ACTIVE_PANE} .ant-collapse-item .actived")
