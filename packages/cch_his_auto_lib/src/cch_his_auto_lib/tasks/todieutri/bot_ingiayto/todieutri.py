from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.tasks.editor import sign_staff_name
from . import _trace, goto


@_trace
def sign_todieutri():
    "Inside *tờ điều trị*, try to sign *tờ điều trị* in sequence"
    _d = get_global_driver()
    main_tab = _d.current_window_handle
    goto(name="Tờ điều trị")
    _d.goto_newtab_do_smth_then_goback(main_tab, sign_staff_name.todieutri)
