from dataclasses import dataclass
from typing import Self
from pathlib import PurePath

from cch_his_auto.common_structs import User, ABCConfig


@dataclass(repr=False, eq=False)
class Config(ABCConfig):
    APP_PATH = PurePath(__file__).parent
    FILEPATH = APP_PATH / "config.json"

    user: User = User()
    department: str = ""
    listing: tuple[int, ...] = ()

    def to_dict(self):
        return {
            "user": self.user.to_dict(),
            "department": self.department,
            "listing": self.listing,
        }

    @classmethod
    def from_dict(cls, value) -> Self:
        return cls(
            User.from_dict(value["user"]), value["department"], tuple(value["listing"])
        )

    def is_valid(self) -> bool:
        return (len(self.department) > 0) and (len(self.listing) > 0)
