from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tasks.editor import sign_staff_name
from . import _trace, goto


# @_trace
# def sign_phieudutrumau(driver: Driver):
#     "try to sign *phiếu dự trù máu*"
#     main_tab = driver.current_window_handle
#     goto(driver, name="Tờ điều trị")
#     driver.goto_newtab_do_smth_then_goback(main_tab, sign_staff_name.todieutri)
