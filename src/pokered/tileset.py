from pathlib import Path

from pydantic import BaseModel

from lapinou.models import TileSet
from pokered.asm import parse_asm_call_file


def parse_tileset_constants(path: Path) -> list[str]:
    return [node.args[0] for node in parse_asm_call_file(path) if node.name == "const"]


class TileSetHeader(BaseModel):
    name: str
    grass_tile: int
    animation: str


def parse_tileset_headers(path: Path) -> list[TileSetHeader]:
    nodes = parse_asm_call_file(path)
    headers = []
    for node in nodes:
        if node.name == "tileset":
            name, _, _, _, grass_tile, animation = node.args
            name = name.lower()
            grass_tile = grass_tile.removeprefix("$")
            grass_tile = int(grass_tile, 16)
            headers.append(
                TileSetHeader(name=name, grass_tile=grass_tile, animation=animation)
            )

    return headers


def parse_tilesets(path: Path) -> list[TileSet]:
    constants = parse_tileset_constants(path / "constants/tileset_constants.asm")
    headers = parse_tileset_headers(path / "data/tilesets/tileset_headers.asm")

    tilesets = []
    for constant, header in zip(constants, headers):
        tilesets.append(
            TileSet(
                id=constant,
                name=header.name,
                grass_tile=header.grass_tile,
                animation=header.animation,
            )
        )

    return tilesets
