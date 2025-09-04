from dataclasses import dataclass
from typing import Self
from pathlib import PurePath

from cch_his_auto.common_structs import User, ABCConfig


@dataclass(repr=False, eq=False, frozen=True)
class Config(ABCConfig):
    APP_PATH = PurePath(__file__).parent
    FILE_PATH = APP_PATH / "config.json"

    user: User = User()
    department: str = ""
    listing: tuple[int, ...] = ()

    @classmethod
    def from_dict(cls, value) -> Self:
        return cls(
            User.from_dict(value["user"]), value["department"], tuple(value["listing"])
        )

    def is_valid(self) -> bool:
        return (len(self.department) > 0) and (len(self.listing) > 0)
