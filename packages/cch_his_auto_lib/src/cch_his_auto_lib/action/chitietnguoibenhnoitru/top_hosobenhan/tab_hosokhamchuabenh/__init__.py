import datetime as dt

from cch_his_auto_lib.driver import Driver
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
from cch_his_auto_lib.action.editor import (
    sign_staff,
    sign_patient,
)


@_trace
def tobiabenhannhikhoa(d: Driver):
    "Filter and sign name: *Tờ bìa bệnh án nhi khoa*"
    filter_check_expand_sign(
        d,
        name="Tờ bìa bệnh án Nhi khoa",
        chuaky_fn=lambda d, i: goto_row_then_tabdo(d, i, sign_staff.tobiabenhannhikhoa),
    )


@_trace
def mucAbenhannhikhoa(d: Driver):
    "Filter and sign name: *Mục A bệnh án nhi khoa*"
    filter_check_expand_sign(
        d,
        name="Mục A - Bệnh án Nhi khoa",
        chuaky_fn=lambda d, i: goto_row_then_tabdo(d, i, sign_staff.mucAbenhannhikhoa),
    )


@_trace
def mucBtongketbenhan(d: Driver):
    "Filter and sign name: *Mục B tổng kết bệnh án*"
    filter_check_expand_sign(
        d,
        name="Mục B - Tổng kết Bệnh án (Nội khoa, Nhi Khoa, Truyền nhiễm, Sơ sinh, Da liễu, DD-PHCN, HHTM)",
        chuaky_fn=lambda d, i: goto_row_then_tabdo(d, i, sign_staff.mucBtongketbenhan),
    )


@_trace
def phieukhambenhvaovien(d: Driver):
    "Filter and sign name: *Phiếu khám bệnh vào viện*"
    filter_check_expand_sign(
        d,
        name="Phiếu khám bệnh vào viện",
        chuaky_fn=sign_current,
    )


@_trace
def phieuchidinhxetnghiem(d: Driver):
    "Filter and sign name: *Phiếu chỉ định xét nghiệm*"
    filter_check_expand_sign(
        d,
        name="Phiếu chỉ định xét nghiệm",
        chuaky_fn=sign_current,
    )


@_trace
def todieutri(d: Driver, _dt: dt.date | None):
    "Filter and sign name: *Tờ điều trị* those before `_dt`"

    def chuaky_fn(i: int):
        if _dt:
            date = dt.datetime.strptime(
                d.find(f".ant-table-tbody tr:nth-child({i}) td:nth-child(2)").text[:10],
                "%d/%m/%Y",
            ).date()
            if date < _dt:
                goto_row_then_tabdo(d, i, sign_staff.todieutri)
            else:
                _lgr.info("=> skip this date")
        else:
            goto_row_then_tabdo(d, i, sign_staff.todieutri)

    filter_check_expand_sign(
        d,
        name="Tờ điều trị",
        chuaky_fn=lambda d, i: chuaky_fn(i),
    )


@_trace
def phieuchidinhPTTT(d: Driver):
    "Filter and sign name: *Phiếu chỉ định PTTT*"
    filter_check_expand_sign(
        d,
        name="Phiếu chỉ định PTTT",
        chuaky_fn=sign_current,
    )


@_trace
def phieuCT(d: Driver, signature: str | None):
    "Filter and sign name: *Phiếu chỉ định chụp CT*"

    def dangky_fn():
        sign_staff.phieuCT_bsthuchien(d)
        if signature:
            sign_patient.phieuCT_bn(d, signature)

    def chuaky_fn():
        sign_staff.phieuCT_bschidinh(d)
        dangky_fn()

    filter_check_expand_sign(
        d,
        name="Phiếu chỉ định chụp cắt lớp vi tính (CT)",
        chuaky_fn=lambda d, i: goto_row_then_tabdo(d, i, chuaky_fn),
        dangky_fn=lambda d, i: goto_row_then_tabdo(d, i, dangky_fn),
    )


@_trace
def phieuMRI(d: Driver, signature: str | None):
    "Filter and sign name: *Phiếu chỉ định chụp MRI*"

    def dangky_fn():
        sign_staff.phieuMRI_bsthuchien(d)
        if signature:
            sign_patient.phieuMRI_bn(d, signature)

    def chuaky_fn():
        sign_staff.phieuMRI_bschidinh(d)
        dangky_fn()

    filter_check_expand_sign(
        d,
        name="Phiếu chỉ định chụp cộng hưởng từ (MRI)",
        chuaky_fn=lambda d, i: goto_row_then_tabdo(d, i, chuaky_fn),
        dangky_fn=lambda d, i: goto_row_then_tabdo(d, i, dangky_fn),
    )


@_trace
def giaiphaubenh(d: Driver):
    "Filter and sign name: *Phiếu xét nghiệm giải phẫu bệnh sinh thiết*"
    filter_check_expand_sign(
        d,
        name="Phiếu xét nghiệm giải phẫu bệnh sinh thiết",
        chuaky_fn=lambda d, i: goto_row_then_tabdo(d, i, sign_staff.giaiphaubenh),
    )


@_trace
def phieusanglocdinhduong(d: Driver):
    "Filter and sign name: *Phiếu sàng lọc dinh dưỡng - Bệnh nhi nội trú*"
    filter_check_expand_sign(
        d,
        name="Phiếu sàng lọc dinh dưỡng - Bệnh nhi nội trú",
        chuaky_fn=sign_current,
    )


@_trace
def phieusoket15ngay(d: Driver):
    "Filter and sign name: *Phiếu sơ kết 15 ngày điều trị*"
    filter_check_expand_sign(
        d,
        name="Phiếu sơ kết 15 ngày điều trị",
        chuaky_fn=sign_current_both,
        dangky_fn=sign_current2,
    )


@_trace
def donthuoc(d: Driver):
    "Filter and sign name: *Đơn thuốc*"
    filter_check_expand_sign(
        d,
        name="Đơn thuốc",
        chuaky_fn=sign_current,
    )


@_trace
def phieucamkettruyenmau(d: Driver, signature: str | None):
    "Filter and sign name: *Phiếu cam kết truyền máu*"

    def chuaky_fn():
        if signature:
            # sign_patient.phieucamkettruyenmau_fill_info_then_sign_bn(d, signature) TODO
            pass

    filter_check_expand_sign(
        d,
        name="Giấy cam đoan chấp nhận truyền máu và các chế phẩm của máu",
        chuaky_fn=lambda d, i: goto_row_then_tabdo(d, i, chuaky_fn),
    )


@_trace
def phieucamkettta5(d: Driver, signature: str | None):
    "Filter and sign name: *Phiếu cam kết thủ thuật a5*"

    def chuaky_fn():
        # sign_staff.phieucamkettta5_fill_info_then_sign(d) TODO
        dangky_fn()

    def dangky_fn():
        if signature:
            sign_patient.phieucamkettta5(d, signature)

    filter_check_expand_sign(
        d,
        name="Giấy cam đoan chấp nhận phẫu thuật, thủ thuật và gây mê hồi sức(của BN) (A5)",
        chuaky_fn=lambda d, i: goto_row_then_tabdo(d, i, chuaky_fn),
        dangky_fn=lambda d, i: goto_row_then_tabdo(d, i, dangky_fn),
    )
