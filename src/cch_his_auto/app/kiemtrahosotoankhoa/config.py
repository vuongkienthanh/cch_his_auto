from dataclasses import dataclass
from typing import Self

from cch_his_auto.common_structs import ABCChildConfig, User, ABCConfig
from pathlib import PurePath


@dataclass(repr=False, eq=False, frozen=True)
class Kytenhosobenhan(ABCChildConfig):
    mucAbenhannhikhoa: bool = True
    phieukhambenhvaovien: bool = True
    phieusanglocdinhduong: bool = True
    phieusoket15ngay: bool = True
    phieuchidinhxetnghiem: bool = True
    phieuCT: bool = True
    phieuMRI: bool = True
    donthuoc: bool = True
    todieutri: bool = True

    @classmethod
    def from_dict(cls, value) -> Self:
        return cls(
            value["mucAbenhannhikhoa"],
            value["phieukhambenhvaovien"],
            value["phieusanglocdinhduong"],
            value["phieusoket15ngay"],
            value["phieuchidinhxetnghiem"],
            value["phieuCT"],
            value["phieuMRI"],
            value["donthuoc"],
            value["todieutri"],
        )


@dataclass(repr=False, eq=False, frozen=True)
class Config(ABCConfig):
    APP_PATH = PurePath(__file__).parent
    FILE_PATH = APP_PATH / "config.json"

    user: User = User()
    department: str = ""
    dinhduong: bool = True
    nhommau: bool = True
    kytenhosobenhan: Kytenhosobenhan = Kytenhosobenhan()

    @classmethod
    def from_dict(cls, value) -> Self:
        return cls(
            User.from_dict(value["user"]),
            value["department"],
            value["dinhduong"],
            value["nhommau"],
            Kytenhosobenhan.from_dict(value["kytenhosobenhan"]),
        )

    def is_valid(self) -> bool:
        return len(self.department) > 0
