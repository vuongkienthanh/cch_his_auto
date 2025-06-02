from cch_his_auto_lib.driver import get_global_driver
from . import ACTIVE_PANE, _lgr

TAB_NUMBER = 2
_lgr = _lgr.getChild("tab_dvkt")

DICHVU_DIALOG_CSS = ".ant-modal:has(.tenDv~.ant-row~.ant-card)"


def get_bloodtype() -> str | None:
    _d = get_global_driver()
    target = "Định nhóm máu hệ ABO, Rh(D) (Kỹ thuật Scangel Gelcard trên máy tự động)"

    _d.clear_input(
        f"{ACTIVE_PANE} .ant-table-header th:nth-child(2) .custom-header-cell:nth-child(2) input"
    ).send_keys(target)
    _d.waiting_to_startswith(
        f"{ACTIVE_PANE} .ant-table-body tr:nth-child(3) td:nth-child(2)", target
    )
    _d.clicking2(f"{ACTIVE_PANE} .ant-table-body tr:nth-child(3) td:last-child svg")
    try:
        abo = _d.waiting(
            f"{DICHVU_DIALOG_CSS} tbody tr:nth-child(7) td:nth-child(2)"
        ).text
        if (
            _d.waiting(
                f"{DICHVU_DIALOG_CSS} tbody tr:nth-child(11) td:nth-child(2)"
            ).text.strip()
            == "DƯƠNG TÍNH"
        ):
            rh = "+"
        else:
            rh = "-"
        return f"{abo}{rh}"
    except:
        return None
    finally:
        _d.clicking(f"{DICHVU_DIALOG_CSS} .ant-modal-close")
