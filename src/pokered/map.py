from collections.abc import Iterable
from pathlib import Path

from pydantic import BaseModel, Field

from lapinou.models import Connection, Map
from pokered.asm import parse_asm_call_file


class MapConstant(BaseModel):
    id: str
    width: int
    height: int


def parse_map_constants(path: Path) -> list[MapConstant]:
    map_constants = []
    for node in parse_asm_call_file(path):
        if node.name == "map_const":
            map_constants.append(
                MapConstant(
                    id=node.args[0], width=int(node.args[1]), height=int(node.args[2])
                )
            )

    return map_constants


def parse_map_header_pointers(path: Path) -> list[str]:
    return [
        node.args[0][:-2] for node in parse_asm_call_file(path) if node.name == "dw"
    ]


class MapHeader(BaseModel):
    name: str
    tileset: str
    connections: list[Connection] = Field(default_factory=list)


def parse_map_header(path: Path) -> MapHeader:
    nodes = parse_asm_call_file(
        path,
    )
    header_node, *connection_nodes, _end_map_node = nodes

    return MapHeader(
        name=header_node.args[0],
        tileset=header_node.args[2],
        connections=[
            Connection(
                side=node.args[0].upper(), map_id=node.args[2], offset=int(node.args[3])
            )
            for node in connection_nodes
        ],
    )


def parse_map_headers(paths: Iterable[Path]) -> list[MapHeader]:
    return [parse_map_header(path) for path in paths]


def parse_maps(path: Path) -> list[Map]:
    constants = parse_map_constants(path / "constants/map_constants.asm")
    pointer_headers = parse_map_header_pointers(
        path / "data/maps/map_header_pointers.asm"
    )
    headers = {
        h.name: h for h in parse_map_headers(path.glob("data/maps/headers/*.asm"))
    }

    maps = []
    for (
        constant,
        map_name,
    ) in zip(constants, pointer_headers):
        if constant.id.startswith("UNUSED_MAP_"):
            continue

        map_header = headers[map_name]

        maps.append(
            Map(
                id=constant.id,
                name=map_name,
                width=constant.width,
                height=constant.height,
                tileset=map_header.tileset,
                connections=map_header.connections,
            )
        )

    return maps
