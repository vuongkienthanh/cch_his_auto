import datetime as dt

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tasks import search_dialog
from cch_his_auto_lib.tasks.editor import sign_staff_name
from . import goto, _trace


@_trace
def sign_phieuCT_bschidinh(driver: Driver, _dt: dt.date):
    goto(driver, "CT")
    search_dialog.filter(driver, _dt.strftime("%d/%m"))
    l= search_dialog.count_item_dropdown(driver) 
    search_dialog.select_item_dropdown(driver, 0)
    search_dialog.save(driver)
    sign_staff_name.phieuCT_bschidinh(driver)
    driver.close()

    if l > 1 :
        for i in range(1, l):
            goto(driver, "CT")
            search_dialog.filter(driver, _dt.strftime("%d/%m"))
            search_dialog.select_item_dropdown(driver, i)
            search_dialog.save(driver)
            sign_staff_name.phieuCT_bschidinh(driver)
            driver.close()
