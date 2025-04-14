from cch_his_auto.driver import Driver
from cch_his_auto.tasks.editor import sign_staff_name
from . import open_menu, goto

def sign_todieutri(driver: Driver):
    "Inside *tờ điều trị*, try to sign *tờ điều trị* in sequence"
    main_tab = driver.current_window_handle
    open_menu(driver)
    goto(driver, name="Tờ điều trị")
    driver.goto_newtab_do_smth_then_goback(main_tab, sign_staff_name.todieutri)
