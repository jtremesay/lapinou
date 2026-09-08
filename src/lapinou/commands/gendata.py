from argparse import ArgumentParser
from collections.abc import Iterable
from pathlib import Path
from shutil import rmtree


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
