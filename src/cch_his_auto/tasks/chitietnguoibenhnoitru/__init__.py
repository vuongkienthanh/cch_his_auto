"""
### Tasks that operate on *Chi tiết người bệnh nội trú*
"""

import time
from cch_his_auto.driver import Driver

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/"
"All tasks in this submodule work under this url."

def scrape_signature(driver: Driver) -> str | None:
    "try getting signature src of current patient"
    from . import indieuduong as idd

    main_tab = driver.current_window_handle
    idd.open(driver)
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
