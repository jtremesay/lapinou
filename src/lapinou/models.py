from enum import StrEnum

from pydantic import BaseModel


class Gender(StrEnum):
    # Vanilla flavors
    MALE = "male"
    FEMALE = "female"

    # Spicy flavors
    # TODO:


class Character(BaseModel):
    name: str
    age: int
    gender: Gender
    occupation: str
    biography: str
    description: str
