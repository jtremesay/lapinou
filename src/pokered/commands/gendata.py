from argparse import ArgumentParser
from collections.abc import Iterable
from pathlib import Path
from shutil import copy, rmtree

from lapinou.models import (
    MapsListAdapter,
    TilesetsListTypeAdapter,
)
from pokered.map import parse_maps
from pokered.tileset import parse_tilesets


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

    ###########################################################################
    # Tilesets
    tilesets = parse_tilesets(input_data_path)

    with (output_data_path / "tilesets.json").open("wb") as f:
        f.write(TilesetsListTypeAdapter.dump_json(tilesets, indent=4))

    output_tilesets_path = output_data_path / "tilesets"
    output_tilesets_path.mkdir(parents=True, exist_ok=True)
    input_tilesets_path = input_data_path / "gfx/tilesets"
    for tileset in tilesets:
        filename = f"{tileset.name}.png"
        input_tileset_path = input_tilesets_path / filename
        output_tileset_path = output_tilesets_path / filename
        if input_tileset_path.exists():
            copy(input_tileset_path, output_tileset_path)

    ###########################################################################
    # Maps
    maps = parse_maps(input_data_path)

    with (output_data_path / "maps.json").open("wb") as f:
        f.write(MapsListAdapter.dump_json(maps, indent=4))
