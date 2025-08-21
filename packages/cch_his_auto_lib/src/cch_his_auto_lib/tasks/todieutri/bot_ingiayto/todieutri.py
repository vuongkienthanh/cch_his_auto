from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tasks.editor import sign_staff
from . import _trace, goto


@_trace
def sign_todieutri(d: Driver):
    "Inside *tờ điều trị*, try to sign *tờ điều trị* in sequence"
    main_tab = d.current_window_handle
    goto(d, name="Tờ điều trị")
    d.goto_newtab_do_smth_then_goback(main_tab, sign_staff.todieutri)
