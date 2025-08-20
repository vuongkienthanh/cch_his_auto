import datetime as dt

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.tracing import tracing
from .. import _lgr

TAB_NUMBER = 1
_lgr = _lgr.getChild("tab_hosokhamchuabenh")
_trace = tracing(_lgr)

from .helper import (
    filter_check_expand_sign,
    goto_row_then_tabdo,
    sign_current,
    sign_current2,
    sign_current_both,
)
from cch_his_auto_lib.tasks.editor import (
    sign_staff_name,
    sign_patient_name,
)


@_trace
def tobiabenhannhikhoa():
    "Filter and sign name: *Tờ bìa bệnh án nhi khoa*"
    filter_check_expand_sign(
        name="Tờ bìa bệnh án Nhi khoa",
        chuaky_fn=lambda i: goto_row_then_tabdo(i, sign_staff_name.tobiabenhannhikhoa),
    )


@_trace
def mucAbenhannhikhoa():
    "Filter and sign name: *Mục A bệnh án nhi khoa*"
    filter_check_expand_sign(
        name="Mục A - Bệnh án Nhi khoa",
        chuaky_fn=lambda i: goto_row_then_tabdo(i, sign_staff_name.mucAbenhannhikhoa),
    )


@_trace
def mucBtongketbenhan():
    "Filter and sign name: *Mục B tổng kết bệnh án*"
    filter_check_expand_sign(
        name="Mục B - Tổng kết Bệnh án (Nội khoa, Nhi Khoa, Truyền nhiễm, Sơ sinh, Da liễu, DD-PHCN, HHTM)",
        chuaky_fn=lambda i: goto_row_then_tabdo(i, sign_staff_name.mucBtongketbenhan),
    )


@_trace
def phieukhambenhvaovien():
    "Filter and sign name: *Phiếu khám bệnh vào viện*"
    filter_check_expand_sign(
        name="Phiếu khám bệnh vào viện",
        chuaky_fn=sign_current,
    )


@_trace
def phieuchidinhxetnghiem():
    "Filter and sign name: *Phiếu chỉ định xét nghiệm*"
    filter_check_expand_sign(
        name="Phiếu chỉ định xét nghiệm",
        chuaky_fn=sign_current,
    )


@_trace
def todieutri(_dt: dt.date | None):
    "Filter and sign name: *Tờ điều trị* those before `_dt`"
    _d = get_global_driver()

    def chuaky_fn(i: int):
        if _dt:
            date = dt.datetime.strptime(
                _d.find(f".ant-table-tbody tr:nth-child({i}) td:nth-child(2)").text[
                    :10
                ],
                "%d/%m/%Y",
            ).date()
            if date < _dt:
                goto_row_then_tabdo(i, sign_staff_name.todieutri)
            else:
                _lgr.info("=> skip this date")
        else:
            goto_row_then_tabdo(i, sign_staff_name.todieutri)

    filter_check_expand_sign(
        name="Tờ điều trị",
        chuaky_fn=lambda i: chuaky_fn(i),
    )


@_trace
def phieuchidinhPTTT():
    "Filter and sign name: *Phiếu chỉ định PTTT*"
    filter_check_expand_sign(
        name="Phiếu chỉ định PTTT",
        chuaky_fn=sign_current,
    )


@_trace
def phieuCT(signature: str | None):
    "Filter and sign name: *Phiếu chỉ định chụp CT*"

    def dangky_fn():
        sign_staff_name.phieuCT_bsthuchien()
        if signature:
            sign_patient_name.phieuCT_bn(signature)

    def chuaky_fn():
        sign_staff_name.phieuCT_bschidinh()
        dangky_fn()

    filter_check_expand_sign(
        name="Phiếu chỉ định chụp cắt lớp vi tính (CT)",
        chuaky_fn=lambda i: goto_row_then_tabdo(i, chuaky_fn),
        dangky_fn=lambda i: goto_row_then_tabdo(i, dangky_fn),
    )


@_trace
def phieuMRI(signature: str | None):
    "Filter and sign name: *Phiếu chỉ định chụp MRI*"

    def dangky_fn():
        sign_staff_name.phieuMRI_bsthuchien()
        if signature:
            sign_patient_name.phieuMRI_bn(signature)

    def chuaky_fn():
        sign_staff_name.phieuMRI_bschidinh()
        dangky_fn()

    filter_check_expand_sign(
        name="Phiếu chỉ định chụp cộng hưởng từ (MRI)",
        chuaky_fn=lambda i: goto_row_then_tabdo(i, chuaky_fn),
        dangky_fn=lambda i: goto_row_then_tabdo(i, dangky_fn),
    )


@_trace
def giaiphaubenh():
    "Filter and sign name: *Phiếu xét nghiệm giải phẫu bệnh sinh thiết*"
    filter_check_expand_sign(
        name="Phiếu xét nghiệm giải phẫu bệnh sinh thiết",
        chuaky_fn=lambda i: goto_row_then_tabdo(i, sign_staff_name.giaiphaubenh),
    )


@_trace
def phieusanglocdinhduong():
    "Filter and sign name: *Phiếu sàng lọc dinh dưỡng - Bệnh nhi nội trú*"
    filter_check_expand_sign(
        name="Phiếu sàng lọc dinh dưỡng - Bệnh nhi nội trú",
        chuaky_fn=sign_current,
    )


@_trace
def phieusoket15ngay():
    "Filter and sign name: *Phiếu sơ kết 15 ngày điều trị*"
    filter_check_expand_sign(
        name="Phiếu sơ kết 15 ngày điều trị",
        chuaky_fn=sign_current_both,
        dangky_fn=sign_current2,
    )


@_trace
def donthuoc():
    "Filter and sign name: *Đơn thuốc*"
    filter_check_expand_sign(
        name="Đơn thuốc",
        chuaky_fn=sign_current,
    )


@_trace
def phieucamkettruyenmau(signature: str | None):
    "Filter and sign name: *Phiếu cam kết truyền máu*"

    def chuaky_fn():
        if signature:
            sign_patient_name.phieucamkettruyenmau_fill_info_then_sign_bn(signature)

    filter_check_expand_sign(
        name="Giấy cam đoan chấp nhận truyền máu và các chế phẩm của máu",
        chuaky_fn=lambda i: goto_row_then_tabdo(i, chuaky_fn),
    )


@_trace
def phieucamkettta5(signature: str | None):
    "Filter and sign name: *Phiếu cam kết thủ thuật a5*"

    def chuaky_fn():
        sign_staff_name.phieucamkettta5_fill_info_then_sign()
        dangky_fn()

    def dangky_fn():
        if signature:
            sign_patient_name.phieucamkettta5(signature)

    filter_check_expand_sign(
        name="Giấy cam đoan chấp nhận phẫu thuật, thủ thuật và gây mê hồi sức(của BN) (A5)",
        chuaky_fn=lambda i: goto_row_then_tabdo(i, chuaky_fn),
        dangky_fn=lambda i: goto_row_then_tabdo(i, dangky_fn),
    )
