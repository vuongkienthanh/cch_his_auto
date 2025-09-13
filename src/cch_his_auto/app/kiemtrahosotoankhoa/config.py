from dataclasses import dataclass
from typing import Self
from cch_his_auto.common_structs import User, ABCConfig
from pathlib import PurePath


@dataclass(repr=False, eq=False, frozen=True)
class Config(ABCConfig):
    APP_PATH = PurePath(__file__).parent
    FILE_PATH = APP_PATH / "config.json"

    user: User = User()
    department: str = ""
    dinhduong: bool = True
    nhommau: bool = True
    kytenhosobenhan: bool = True

    @classmethod
    def from_dict(cls, value) -> Self:
        return cls(
            User.from_dict(value["user"]),
            value["department"],
            value["dinhduong"],
            value["nhommau"],
            value["kytenhosobenhan"],
        )

    def is_valid(self) -> bool:
        return len(self.department) > 0
