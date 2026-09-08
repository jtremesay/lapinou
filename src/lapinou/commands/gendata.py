from argparse import ArgumentParser
from collections.abc import Iterable
from pathlib import Path
from shutil import rmtree

from lapinou.models import Connection, Map, MapKind, MapTypeAdapter


def main(args: Iterable[str] | None = None):
    parser = ArgumentParser()
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="Clean the output directory before generating data",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("thirds/pokered"),
        help="Path to the input file",
    )
    parser.add_argument(
        "--output", type=Path, default=Path("data"), help="Path to the output file"
    )
    parsed_args = parser.parse_args(args)

    input_data_path = parsed_args.input
    output_data_path = parsed_args.output

    # Clean and create the output directory if needed
    if parsed_args.clean:
        rmtree(output_data_path, ignore_errors=True)
    output_data_path.mkdir(parents=True, exist_ok=True)

    # Maps constants
    # Idx and orders should be the same as in the input file because the
    # constants are used as idx in pointer tables
    # The filtering of unused maps should be done later in the pipeline
    map_constansts: list[tuple[str, MapKind, int, int]] = []
    with (input_data_path / "constants/map_constants.asm").open("r") as f:
        map_kind = MapKind.CITY
        for l in f:
            # Remove comments and strip whitespace
            l = l.split(";", 1)[0].strip()

            # Process map constants
            if l.startswith("map_const"):
                l = l[10:]
                map_id, map_width, map_height = list(map(str.strip, l.split(",")))
                map_width = int(map_width)
                map_height = int(map_height)
                map_constansts.append((map_id, map_kind, map_width, map_height))
            elif l.startswith("DEF FIRST_ROUTE_MAP"):
                map_kind = MapKind.ROAD
            elif l.startswith("DEF FIRST_INDOOR_MAP"):
                map_kind = MapKind.INDOOR

    # Maps pointer table
    # mapping from map_idx to map_name
    map_pointers: list[str] = []
    with (input_data_path / "data/maps/map_header_pointers.asm").open("r") as f:
        # Move to the start of the table by skipping lines until "table_width" is foundo
        for l in f:
            if l.lstrip().startswith("table_width"):
                break

        for l in f:
            l = l.split(";", 1)[0].strip()
            if not l:
                continue

            if not l.startswith("dw "):
                break

            map_name = l[3:][:-2]
            map_pointers.append(map_name)

    # Maps headers
    map_headers: dict[str, tuple[str, str, list[Connection]]] = {}
    for e in input_data_path.glob("data/maps/headers/*.asm"):
        with e.open("r") as f:
            l = next(f).strip()
            assert l.startswith("map_header "), f"Unexpected line: {l}"
            map_name, map_id, map_tileset = list(map(str.strip, l[11:].split(",")))

            # Parse connections
            connections: list[Connection] = []
            for l in f:
                l = l.split(";", 1)[0].strip()
                if not l:
                    continue

                if l.startswith("connection "):
                    side, _other_map_name, other_map_id, offset = list(
                        map(str.strip, l[11:].split(","))
                    )
                    side = side.upper()
                    offset = int(offset)
                    connections.append(
                        Connection(side=side, map_id=other_map_id, offset=offset)
                    )

            map_headers[map_name] = (map_id, map_tileset, connections)

    # Build the list of Map objects
    maps = []
    for (
        (map_id, map_kind, map_width, map_height),
        map_name,
    ) in zip(map_constansts, map_pointers):
        if map_id.startswith("UNUSED_MAP_"):
            continue

        _map_id, map_tileset, connections = map_headers[map_name]
        maps.append(
            Map(
                id=map_id,
                name=map_name,
                kind=map_kind,
                width=map_width,
                height=map_height,
                tileset=map_tileset,
                connections=connections,
            )
        )

    # Serialize maps to JSON using MapTypeAdapter
    with (output_data_path / "maps.json").open("wb") as f:
        f.write(MapTypeAdapter.dump_json(maps, indent=4))
