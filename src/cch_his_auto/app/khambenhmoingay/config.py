from dataclasses import dataclass
from pathlib import PurePath
from typing import Self
from validators import url

from cch_his_auto.common_structs import User, ABCConfig


type k3 = tuple[bool, bool, bool, bool, bool]
k3_default = (False, False, False, False, False)


@dataclass(eq=False, repr=False, frozen=True)
class Ky_3tra:
    bacsi: k3 = k3_default
    dieuduong: k3 = k3_default
    benhnhan: k3 = k3_default

    def to_dict(self):
        return {
            "bacsi": self.bacsi,
            "dieuduong": self.dieuduong,
            "benhnhan": self.benhnhan,
        }

    @classmethod
    def from_dict(cls, value) -> Self:
        return cls(value["bacsi"], value["dieuduong"], value["benhnhan"])


@dataclass(eq=False, repr=False, frozen=True)
class Todieutri:
    url: str = ""
    note: str = ""
    ky_xn: bool = False
    ky_todieutri: bool = True
    ky_3tra: Ky_3tra = Ky_3tra()

    def to_dict(self):
        return {
            "url": self.url,
            "note": self.note,
            "ky_xn": self.ky_xn,
            "ky_todieutri": self.ky_todieutri,
            "ky_3tra": self.ky_3tra.to_dict(),
        }

    @classmethod
    def from_dict(cls, value) -> Self:
        return cls(
            value["url"],
            value["note"],
            value["ky_xn"],
            value["ky_todieutri"],
            Ky_3tra.from_dict(value["ky_3tra"]),
        )


@dataclass(eq=False, repr=False, frozen=True)
class Bienbanhoichan:
    url: str = ""
    note: str = ""
    ky_thuky: bool = False
    ky_truongkhoa: bool = False
    ky_thanhvienkhac: bool = False
    khac_note: str = ""

    def to_dict(self):
        return {
            "url": self.url,
            "note": self.note,
            "ky_thuky": self.ky_thuky,
            "ky_truongkhoa": self.ky_truongkhoa,
            "ky_thanhvienkhac": self.ky_thanhvienkhac,
            "khac_note": self.khac_note,
        }

    @classmethod
    def from_dict(cls, value) -> Self:
        return cls(
            value["url"],
            value["note"],
            value["ky_thuky"],
            value["ky_truongkhoa"],
            value["ky_thanhvienkhac"],
            value["khac_note"],
        )


@dataclass(eq=False, repr=False, frozen=True)
class Config(ABCConfig):
    APP_PATH = PurePath(__file__).parent
    FILEPATH = APP_PATH / "config.json"

    bacsi: User = User()
    dieuduong: User = User()
    truongkhoa: User = User()
    thanhvienkhac: User = User()
    department: str = ""
    todieutri: tuple[Todieutri, ...] = ()
    bienbanhoichan: tuple[Bienbanhoichan, ...] = ()

    def to_dict(self):
        return {
            "bacsi": self.bacsi.to_dict(),
            "dieuduong": self.dieuduong.to_dict(),
            "truongkhoa": self.truongkhoa.to_dict(),
            "thanhvienkhac": self.thanhvienkhac.to_dict(),
            "department": self.department,
            "todieutri": [tdt.to_dict() for tdt in self.todieutri],
            "bienbanhoichan": [bbhc.to_dict() for bbhc in self.bienbanhoichan],
        }

    @classmethod
    def from_dict(cls, value) -> Self:
        return cls(
            User.from_dict(value["bacsi"]),
            User.from_dict(value["dieuduong"]),
            User.from_dict(value["truongkhoa"]),
            User.from_dict(value["thanhvienkhac"]),
            value["department"],
            tuple(Todieutri.from_dict(v) for v in value["todieutri"]),
            tuple(Bienbanhoichan.from_dict(v) for v in value["bienbanhoichan"]),
        )

    def is_valid(self) -> bool:
        return (
            (len(self.department) > 0)
            and ((len(self.todieutri) + len(self.bienbanhoichan)) > 0)
            and all(
                url(tdt.url) and ("chi-tiet-nguoi-benh-noi-tru/to-dieu-tri/" in tdt.url)
                for tdt in self.todieutri
            )
            and all(
                url(bbhc.url)
                and ("chi-tiet-nguoi-benh-noi-tru/bien-ban-hoi-chan/" in bbhc.url)
                for bbhc in self.bienbanhoichan
            )
        )
