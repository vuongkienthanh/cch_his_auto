from selenium.common import NoSuchElementException
from cch_his_auto_lib.driver import Driver
from . import ACTIVE_PANE, _lgr

TAB_NUMBER = 2
_lgr = _lgr.getChild("tab_dvkt")

DICHVU_DIALOG_CSS = ".ant-modal:has(.tenDv~.ant-row~.ant-card)"


def get_bloodtype(d: Driver) -> str | None:
    target = "Định nhóm máu hệ ABO, Rh(D) (Kỹ thuật Scangel Gelcard trên máy tự động)"

    d.clear_input(
        f"{ACTIVE_PANE} .ant-table-header th:nth-child(3) .custom-header-cell:nth-child(2) input"
    ).send_keys(target)
    try:
        d.waiting_to_startswith(
            f"{ACTIVE_PANE} .ant-table-body tr:nth-child(3) td:nth-child(3)", target
        )
    except NoSuchElementException:
        _lgr.warning("There is no bloodtype lab test")
        return None
    d.clicking2(f"{ACTIVE_PANE} .ant-table-body tr:nth-child(3) td:last-child svg")
    try:
        abo = d.waiting(
            f"{DICHVU_DIALOG_CSS} tbody tr:nth-child(8) td:nth-child(2)"
        ).text.strip()
        if abo == "KHÔNG XÁC ĐỊNH":
            return None

        if (
            d.waiting(
                f"{DICHVU_DIALOG_CSS} tbody tr:nth-child(12) td:nth-child(2)"
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
        d.clicking(f"{DICHVU_DIALOG_CSS} .ant-modal-close")
