from enum import StrEnum

from pydantic import BaseModel


class MapKind(StrEnum):
    CITY = "CITY"
    ROAD = "ROAD"
    INDOOR = "INDOOR"


class Map(BaseModel):
    name: str
    kind: MapKind
    width: int
    height: int
