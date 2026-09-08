from enum import StrEnum

from pydantic import BaseModel, Field, TypeAdapter


class MapKind(StrEnum):
    CITY = "CITY"
    ROAD = "ROAD"
    INDOOR = "INDOOR"


class Direction(StrEnum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


class Connection(BaseModel):
    side: Direction
    map_id: str
    offset: int


class Map(BaseModel):
    id: str
    name: str
    kind: MapKind
    width: int
    height: int
    tileset: str
    connections: list[Connection] = Field(default_factory=list)


MapTypeAdapter = TypeAdapter(list[Map])
