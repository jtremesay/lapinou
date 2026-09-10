from enum import StrEnum

from pydantic import BaseModel, Field, TypeAdapter


class TileSet(BaseModel):
    id: str
    name: str
    grass_tile: int = -1
    animation: str = "TILEANIM_NONE"


TileSetsListTypeAdapter = TypeAdapter(list[TileSet])


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
    width: int
    height: int
    tileset: str
    connections: list[Connection] = Field(default_factory=list)


MapsListAdapter = TypeAdapter(list[Map])
