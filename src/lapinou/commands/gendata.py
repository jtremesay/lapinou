from argparse import ArgumentParser
from collections.abc import Iterable
from pathlib import Path
from shutil import rmtree

from lapinou.models import MapKind


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
    map_constansts: dict[str, tuple[MapKind, int, int]] = {}
    with (input_data_path / "constants/map_constants.asm").open("r") as f:
        map_kind = MapKind.CITY
        for l in f:
            # Remove comments and strip whitespace
            l = l.split(";", 1)[0].strip()

            # Process map constants
            if l.startswith("map_const"):
                l = l[10:]

                map_id, map_width, map_height = l.split(",")
                if map_id.startswith("UNUSED_MAP_"):
                    continue

                map_width = int(map_width)
                map_height = int(map_height)
                # print(f"Map: {map_id}, Width: {map_width}, Height: {map_height}")
                map_constansts[map_id] = (map_kind, map_width, map_height)
            elif l.startswith("DEF FIRST_ROUTE_MAP"):
                map_kind = MapKind.ROAD
            elif l.startswith("DEF FIRST_INDOOR_MAP"):
                map_kind = MapKind.INDOOR
    print(map_constansts)
