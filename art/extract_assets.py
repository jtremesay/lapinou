#!/usr/bin/env python3
import shutil
from argparse import ArgumentParser
from collections.abc import Iterable
from pathlib import Path
from zipfile import ZipFile

from tqdm import tqdm

DEFAULT_ASSETS_DIR = (
    Path(__file__).parent.parent / "src" / "lapinou" / "game" / "assets"
)


class ZipFileExtractAction:
    def __init__(self, zip_file: ZipFile, entry_name: str, out_path: Path):
        self.zip_file = zip_file
        self.entry_name = entry_name
        self.out_path = out_path

    def __call__(self, *args, **kwargs):
        self.out_path.parent.mkdir(parents=True, exist_ok=True)
        with (
            self.zip_file.open(self.entry_name) as entry,
            self.out_path.open("wb") as out_file,
        ):
            shutil.copyfileobj(entry, out_file)


def extract_sprout_ui(sprout_ui_zip: Path, assets_dir: Path):
    sprout_ui_dir = assets_dir / "sprout" / "ui"
    shutil.rmtree(sprout_ui_dir, ignore_errors=True)
    sprout_ui_dir.mkdir(parents=True, exist_ok=True)

    with ZipFile(sprout_ui_zip, "r") as zip_file:
        actions = [
            ZipFileExtractAction(
                zip_file,
                "Sprout Lands - UI Pack - Basic pack/fonts/pixelFont-7-8x14-sproutLands.ttf",
                sprout_ui_dir / "fonts" / "font_8x14.ttf",
            ),
            ZipFileExtractAction(
                zip_file,
                "Sprout Lands - UI Pack - Basic pack/fonts/pixel-letters-7-8x14.png",
                sprout_ui_dir / "fonts" / "font_8x14.png",
            ),
        ]
        for action in tqdm(actions, desc="Extracting Sprout UI assets", unit="file"):
            action()


def main(args: Iterable[str] | None = None) -> None:
    parser = ArgumentParser(description="Extract assets from a game.")
    parser.add_argument(
        "--sprout-ui",
        type=Path,
        default="Sprout Lands - UI Pack - Basic pack.zip",
        help="Path to the Sprout UI zip file.",
    )
    parser.add_argument(
        "-a",
        "--assets-dir",
        type=Path,
        default=DEFAULT_ASSETS_DIR,
        help="Directory in which to extract the assets.",
    )
    parsed_args = parser.parse_args(args)

    extract_sprout_ui(parsed_args.sprout_ui, parsed_args.assets_dir)


if __name__ == "__main__":
    main()
