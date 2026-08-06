from dataclasses import dataclass
from enum import StrEnum


class Gender(StrEnum):
    # Vanilla flavors
    MALE = "male"
    FEMALE = "female"

    # Spicy flavors
    # TODO:


@dataclass
class Character:
    name: str
    age: int
    gender: Gender
    occupation: str
    biography: str
    description: str
