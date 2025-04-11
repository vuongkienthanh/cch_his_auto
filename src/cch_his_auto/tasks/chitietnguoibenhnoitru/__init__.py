"""
### Tasks that operate on *Chi tiết người bệnh nội trú*
"""

import time
import datetime as dt

from cch_his_auto.driver import Driver

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/"
"All tasks in this submodule work under this url."

def scrape_signature(driver: Driver) -> str | None:
    "try getting signature src of current patient"
    from . import indieuduong as idd

    main_tab = driver.current_window_handle
    idd.open_menu(driver)
    idd.goto(driver, "cam kết chung về nhập viện")
    driver.goto_newtab(main_tab)
    try:
        ele = driver.waiting(".layout-line-item:nth-child(43) img")
        ans = ele.get_dom_attribute("src").strip()
        return ans
    except:
        return None
    finally:
        driver.close()
        driver.switch_to.window(main_tab)
        time.sleep(5)

def get_admission_date(driver: Driver) -> dt.date:
    return dt.datetime.strptime(
        driver.waiting(
            ".tab-box .content-tab .ant-row .ant-col:nth-child(2) .item-sub b",
            "admission date",
        ).text,
        "%d/%m/%Y %H:%M:%S",
    ).date()
