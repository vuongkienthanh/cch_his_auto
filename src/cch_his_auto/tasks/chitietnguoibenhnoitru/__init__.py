"""
### Tasks that operate on *Chi tiết người bệnh nội trú*
"""

import time
from cch_his_auto.driver import Driver

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/"
"All tasks in this submodule work under this url."

def get_signature_from_web(driver: Driver) -> str:
    "get signature src of current patient"
    from .indieuduong import open, goto, close

    main_tab = driver.current_window_handle
    open(driver)
    goto(driver, "cam kết chung về nhập viện")
    driver.goto_newtab(main_tab)
    ele = driver.waiting(".layout-line-item:nth-child(43) img")
    ans = ele.get_dom_attribute("src").strip()
    driver.close()
    driver.switch_to.window(main_tab)
    close(driver)
    time.sleep(1)
    return ans
