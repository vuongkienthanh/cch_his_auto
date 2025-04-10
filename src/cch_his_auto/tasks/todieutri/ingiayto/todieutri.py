from cch_his_auto.driver import Driver
from cch_his_auto.tasks.editor import sign_staff_name
from . import open_menu, goto

def todieutri(driver: Driver):
    main_tab = driver.current_window_handle
    try:
        open_menu(driver)
        goto(driver, name="Tờ điều trị")
    except:
        return
    else:
        driver.goto_newtab_do_smth_then_goback(main_tab, sign_staff_name.todieutri)
