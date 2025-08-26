from rich import print

from cch_his_auto_lib.action.todieutri import bot_ingiayto
from cch_his_auto_lib.driver import Driver


def sign_phieuchidinh(d: Driver):
    bot_ingiayto.phieuchidinh.sign_phieuchidinh(d)


def sign_todieutri(d: Driver):
    bot_ingiayto.todieutri.sign_todieutri(d)


def sign_phieuthuchienylenh_bs(d: Driver, arr: tuple[bool, bool, bool, bool, bool]):
    print("[red]++++ doing phieuthuchienylenh_bs, may take a while")
    bot_ingiayto.phieuthuchienylenh.sign_phieuthuchienylenh_bs(d, arr)


def sign_phieuthuchienylenh_dd(d: Driver, arr: tuple[bool, bool, bool, bool, bool]):
    print("[red]++++ doing phieuthuchienylenh_dd, may take a while")
    bot_ingiayto.phieuthuchienylenh.sign_phieuthuchienylenh_dd(d, arr)


def sign_phieuthuchienylenh_bn(
    d: Driver, arr: tuple[bool, bool, bool, bool, bool], signature: str
):
    print("[red]++++ doing phieuthuchienylenh_bs, may take a while")
    bot_ingiayto.phieuthuchienylenh.sign_phieuthuchienylenh_bn(d, arr, signature)
