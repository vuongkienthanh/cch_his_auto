from cch_his_auto_lib.driver import Driver
from . import wait_loaded


def bs(d: Driver, arr: tuple[bool, bool, bool, bool, bool]):
    "*Phiếu thực hiện y lệnh (bác sĩ)*"
    wait_loaded(d)
    d.waiting(".table-tbody")
    for col in map(lambda x: x[0], filter(lambda x: x[1], zip([3, 4, 5, 6, 7], arr))):
        d.sign_staff_signature(
            btn_css=f"table tbody tr:nth-last-child(4) td:nth-child({col}) button",
            btn_txt="Ký",
            img_css=f"table tbody tr:nth-last-child(4) td:nth-child({col}) img",
            name="phieu thuc hien y lenh bac si row 1",
        )
        d.sign_staff_signature(
            btn_css=f"table tbody tr:nth-last-child(3) td:nth-child({col}) button",
            btn_txt="Ký",
            img_css=f"table tbody tr:nth-last-child(3) td:nth-child({col}) img",
            name="phieu thuc hien y lenh bac si row 2",
        )


def dd(d: Driver, arr: tuple[bool, bool, bool, bool, bool]):
    "*Phiếu thực hiện y lệnh (điều dưỡng)*"
    wait_loaded(d)
    d.waiting(".table-tbody")
    for col in map(lambda x: x[0], filter(lambda x: x[1], zip([3, 4, 5, 6, 7], arr))):
        d.sign_staff_signature(
            btn_css=f"table tbody tr:nth-last-child(2) td:nth-child({col}) button",
            btn_txt="Ký",
            img_css=f"table tbody tr:nth-last-child(2) td:nth-child({col}) img",
            name="phieu thuc hien y lenh dieu duong",
        )


def bn(d: Driver, arr: tuple[bool, bool, bool, bool, bool], signature: str | None):
    "*Phiếu thực hiện y lệnh (bệnh nhân)*"
    if signature is None:
        return
    wait_loaded(d)
    d.waiting(".table-tbody")
    for col in map(lambda x: x[0], filter(lambda x: x[1], zip([3, 4, 5, 6, 7], arr))):
        d.sign_patient_signature(
            btn_css=f"table tbody tr:nth-last-child(1) td:nth-child({col}) button",
            btn_txt="Ký",
            img_css=f"table tbody tr:nth-last-child(1) td:nth-child({col}) img",
            signature=signature,
            name=f"row 4 col {col - 2}",
        )
