from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action.editor import (
    tobiabenhannhikhoa as editor_tobiabenhannhikhoa,
    mucAbenhannhikhoa as editor_mucAbenhannhikhoa,
    mucBtongketbenhan as editor_mucBtongketbenhan,
    todieutri as editor_todieutri,
    giaiphaubenh as editor_giaiphaubenh,
    CT as editor_CT,
    MRI as editor_MRI,
)
from ._sign import (
    filter_check_expand_sign,
    goto_row_and_click_edit,
    sign_current,
    sign_current2,
    sign_current_both,
)


def tobiabenhannhikhoa(d: Driver):
    "Filter and sign name: *Tờ bìa bệnh án nhi khoa*"

    def chuaky_fn(d: Driver, i: int):
        d.do_next_tab_do(
            f1=lambda d: goto_row_and_click_edit(d, i), f2=editor_tobiabenhannhikhoa.bs
        )

    filter_check_expand_sign(d, "Tờ bìa bệnh án Nhi khoa", chuaky_fn)


def mucAbenhannhikhoa(d: Driver):
    "Filter and sign name: *Mục A bệnh án nhi khoa*"

    def chuaky_fn(d: Driver, i: int):
        d.do_next_tab_do(
            f1=lambda d: goto_row_and_click_edit(d, i), f2=editor_mucAbenhannhikhoa.bs
        )

    filter_check_expand_sign(d, "Mục A - Bệnh án Nhi khoa", chuaky_fn)


def mucBtongketbenhan(d: Driver):
    "Filter and sign name: *Mục B tổng kết bệnh án*"

    def chuaky_fn(d: Driver, i: int):
        d.do_next_tab_do(
            f1=lambda d: goto_row_and_click_edit(d, i), f2=editor_mucBtongketbenhan.bs
        )

    filter_check_expand_sign(
        d,
        "Mục B - Tổng kết Bệnh án (Nội khoa, Nhi Khoa, Truyền nhiễm, Sơ sinh, Da liễu, DD-PHCN, HHTM)",
        chuaky_fn,
    )


def phieukhambenhvaovien(d: Driver):
    "Filter and sign name: *Phiếu khám bệnh vào viện*"
    filter_check_expand_sign(d, "Phiếu khám bệnh vào viện", sign_current)


def phieuchidinhxetnghiem(d: Driver):
    "Filter and sign name: *Phiếu chỉ định xét nghiệm*"
    filter_check_expand_sign(d, "Phiếu chỉ định xét nghiệm", sign_current)


def todieutri(d: Driver):
    "Filter and sign name: *Tờ điều trị* those before `_dt`"

    def chuaky_fn(d: Driver, i: int):
        d.do_next_tab_do(
            f1=lambda d: goto_row_and_click_edit(d, i), f2=editor_todieutri.bs
        )

    filter_check_expand_sign(d, "Tờ điều trị", chuaky_fn)


def phieuchidinhPTTT(d: Driver):
    "Filter and sign name: *Phiếu chỉ định PTTT*"
    filter_check_expand_sign(d, "Phiếu chỉ định PTTT", sign_current)


def phieuCT(d: Driver, signature: str | None = None):
    "Filter and sign name: *Phiếu chỉ định chụp CT*"

    def chuaky_fn(d: Driver, i: int):
        def f2_fn(d: Driver):
            editor_CT.bschidinh(d)
            editor_CT.bsthuchien(d)
            if signature:
                editor_CT.bn(d, signature)

        d.do_next_tab_do(f1=lambda d: goto_row_and_click_edit(d, i), f2=f2_fn)

    def dangky_fn(d: Driver, i: int):
        def f2_fn(d: Driver):
            editor_CT.bsthuchien(d)
            if signature:
                editor_CT.bn(d, signature)

        d.do_next_tab_do(f1=lambda d: goto_row_and_click_edit(d, i), f2=f2_fn)

    filter_check_expand_sign(
        d, "Phiếu chỉ định chụp cắt lớp vi tính (CT)", chuaky_fn, dangky_fn
    )


def phieuMRI(d: Driver, signature: str | None = None):
    "Filter and sign name: *Phiếu chỉ định chụp MRI*"

    def chuaky_fn(d: Driver, i: int):
        def f2_fn(d: Driver):
            editor_MRI.bschidinh(d)
            editor_MRI.bsthuchien(d)
            if signature:
                editor_MRI.bn(d, signature)

        d.do_next_tab_do(f1=lambda d: goto_row_and_click_edit(d, i), f2=f2_fn)

    def dangky_fn(d: Driver, i: int):
        def f2_fn(d: Driver):
            editor_MRI.bsthuchien(d)
            if signature:
                editor_MRI.bn(d, signature)

        d.do_next_tab_do(f1=lambda d: goto_row_and_click_edit(d, i), f2=f2_fn)

    filter_check_expand_sign(
        d, "Phiếu chỉ định chụp cộng hưởng từ (MRI)", chuaky_fn, dangky_fn
    )


def giaiphaubenh(d: Driver):
    "Filter and sign name: *Phiếu xét nghiệm giải phẫu bệnh sinh thiết*"

    def chuaky_fn(d: Driver, i: int):
        d.do_next_tab_do(
            f1=lambda d: goto_row_and_click_edit(d, i), f2=editor_giaiphaubenh.bs
        )

    filter_check_expand_sign(d, "Phiếu xét nghiệm giải phẫu bệnh sinh thiết", chuaky_fn)


def phieusanglocdinhduong(d: Driver):
    "Filter and sign name: *Phiếu sàng lọc dinh dưỡng - Bệnh nhi nội trú*"
    filter_check_expand_sign(
        d, "Phiếu sàng lọc dinh dưỡng - Bệnh nhi nội trú", sign_current
    )


def phieusoket15ngay(d: Driver):
    "Filter and sign name: *Phiếu sơ kết 15 ngày điều trị*"
    filter_check_expand_sign(
        d, "Phiếu sơ kết 15 ngày điều trị", sign_current_both, sign_current2
    )


def donthuoc(d: Driver):
    "Filter and sign name: *Đơn thuốc*"
    filter_check_expand_sign(d, "Đơn thuốc", sign_current)


# @_trace
# def phieucamkettruyenmau(d: Driver, signature: str | None):
#     "Filter and sign name: *Phiếu cam kết truyền máu*"
#
#     def chuaky_fn():
#         if signature:
#             # sign_patient.phieucamkettruyenmau_fill_info_then_sign_bn(d, signature) TODO
#             pass
#
#     filter_check_expand_sign(
#         d,
#         name="Giấy cam đoan chấp nhận truyền máu và các chế phẩm của máu",
#         chuaky_fn=lambda d, i: goto_row_then_tabdo(d, i, chuaky_fn),
#     )


# @_trace
# def phieucamkettta5(d: Driver, signature: str | None):
#     "Filter and sign name: *Phiếu cam kết thủ thuật a5*"
#
#     def chuaky_fn():
#         # sign_staff.phieucamkettta5_fill_info_then_sign(d) TODO
#         dangky_fn()
#
#     def dangky_fn():
#         if signature:
#             sign_patient.phieucamkettta5(d, signature)
#
#     filter_check_expand_sign(
#         d,
#         name="Giấy cam đoan chấp nhận phẫu thuật, thủ thuật và gây mê hồi sức(của BN) (A5)",
#         chuaky_fn=lambda d, i: goto_row_then_tabdo(d, i, chuaky_fn),
#         dangky_fn=lambda d, i: goto_row_then_tabdo(d, i, dangky_fn),
#     )
