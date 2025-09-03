from dataclasses import dataclass
from pathlib import PurePath
from typing import ClassVar, Self
from abc import ABC, abstractmethod
import os
import json


@dataclass(repr=False, eq=False)
class User:
    name: str = ""
    password: str = ""

    def is_valid(self) -> bool:
        return self.name != "" and self.password != ""

    def to_dict(self):
        return {"name": self.name, "password": self.password}

    @classmethod
    def from_dict(cls, value) -> Self:
        return cls(value["name"], value["password"])


@dataclass(repr=False, eq=False, frozen=True)
class ABCConfig(ABC):
    APP_PATH: ClassVar[PurePath]
    FILE_PATH: ClassVar[PurePath]

    @abstractmethod
    def to_dict(self): ...

    @classmethod
    @abstractmethod
    def from_dict(cls, value) -> Self: ...

    @abstractmethod
    def is_valid(self) -> bool: ...
    def save(self):
        os.makedirs(self.APP_PATH, exist_ok=True)
        with open(self.FILE_PATH, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def load(cls) -> Self:
        try:
            with open(cls.FILE_PATH, "r") as f:
                return cls.from_dict(json.load(f))
        except Exception as _:
            return cls()
