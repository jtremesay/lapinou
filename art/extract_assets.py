#!/usr/bin/env python3
import logging
import shutil
from argparse import ArgumentParser
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from zipfile import ZipFile

from PIL import Image

from lapinou.assets import DIR as ASSETS_DIR

logger = logging.getLogger(__name__)


@dataclass
class NinePatch:
    left_width: int
    right_width: int
    top_height: int
    bottom_height: int
    center_width: int
    center_height: int
    in_offset_x: int = 0
    in_offset_y: int = 0
    out_center_width: int = 1
    out_center_height: int = 1
    out_offset_x: int = 0
    out_offset_y: int = 0

    @property
    def in_width(self) -> int:
        return self.left_width + self.center_width + self.right_width

    @property
    def in_height(self) -> int:
        return self.top_height + self.center_height + self.bottom_height

    @property
    def in_size(self) -> tuple[int, int]:
        return (self.in_width, self.in_height)

    @property
    def out_width(self) -> int:
        return self.left_width + self.out_center_width + self.right_width

    @property
    def out_height(self) -> int:
        return self.top_height + self.out_center_height + self.bottom_height

    @property
    def out_size(self) -> tuple[int, int]:
        return (self.out_width, self.out_height)

    @property
    def in_left(self) -> int:
        return self.in_offset_x

    @property
    def in_center_left(self) -> int:
        return self.in_left + self.left_width

    @property
    def in_center_right(self) -> int:
        return self.in_center_left + self.center_width

    @property
    def in_right(self) -> int:
        return self.in_center_right + self.right_width

    @property
    def in_top(self) -> int:
        return self.in_offset_y

    @property
    def in_center_top(self) -> int:
        return self.in_top + self.top_height

    @property
    def in_center_bottom(self) -> int:
        return self.in_center_top + self.center_height

    @property
    def in_bottom(self) -> int:
        return self.in_center_bottom + self.bottom_height

    @property
    def out_left(self) -> int:
        return self.out_offset_x

    @property
    def out_center_left(self) -> int:
        return self.out_left + self.left_width

    @property
    def out_center_right(self) -> int:
        return self.out_center_left + self.out_center_width

    @property
    def out_right(self) -> int:
        return self.out_center_right + self.right_width

    @property
    def out_top(self) -> int:
        return self.out_offset_y

    @property
    def out_center_top(self) -> int:
        return self.out_top + self.top_height

    @property
    def out_center_bottom(self) -> int:
        return self.out_center_top + self.out_center_height

    @property
    def out_bottom(self) -> int:
        return self.out_center_bottom + self.bottom_height

    @property
    def in_boxes(self) -> list[tuple[int, int, int, int]]:
        return [
            # Top-left
            (self.in_left, self.in_top, self.in_center_left, self.in_center_top),
            # Top
            (
                self.in_center_left,
                self.in_top,
                self.in_center_left + self.out_center_width,
                self.in_center_top,
            ),
            # Top-right
            (self.in_center_right, self.in_top, self.in_right, self.in_center_top),
            # Left
            (
                self.in_left,
                self.in_center_top,
                self.in_center_left,
                self.in_center_top + self.out_center_height,
            ),
            # Center
            (
                self.in_center_left,
                self.in_center_top,
                self.in_center_left + self.out_center_width,
                self.in_center_top + self.out_center_height,
            ),
            # Right
            (
                self.in_center_right,
                self.in_center_top,
                self.in_right,
                self.in_center_top + self.out_center_height,
            ),
            # Bottom-left
            (self.in_left, self.in_center_bottom, self.in_center_left, self.in_bottom),
            # Bottom
            (
                self.in_center_left,
                self.in_center_bottom,
                self.in_center_left + self.out_center_width,
                self.in_bottom,
            ),
            # Bottom-right
            (
                self.in_center_right,
                self.in_center_bottom,
                self.in_right,
                self.in_bottom,
            ),
        ]

    @property
    def out_boxes(self) -> list[tuple[int, int, int, int]]:
        return [
            # Top-left
            (self.out_left, self.out_top, self.out_center_left, self.out_center_top),
            # Top
            (
                self.out_center_left,
                self.out_top,
                self.out_center_right,
                self.out_center_top,
            ),
            # Top-right
            (
                self.out_center_right,
                self.out_top,
                self.out_right,
                self.out_center_top,
            ),
            # Left
            (
                self.out_left,
                self.out_center_top,
                self.out_center_left,
                self.out_center_bottom,
            ),
            # Center
            (
                self.out_center_left,
                self.out_center_top,
                self.out_center_right,
                self.out_center_bottom,
            ),
            # Right
            (
                self.out_center_right,
                self.out_center_top,
                self.out_right,
                self.out_center_bottom,
            ),
            # Bottom-left
            (
                self.out_left,
                self.out_center_bottom,
                self.out_center_left,
                self.out_bottom,
            ),
            # Bottom
            (
                self.out_center_left,
                self.out_center_bottom,
                self.out_center_right,
                self.out_bottom,
            ),
            # Bottom-right
            (
                self.out_center_right,
                self.out_center_bottom,
                self.out_right,
                self.out_bottom,
            ),
        ]

    @property
    def boxes(
        self,
    ) -> list[tuple[tuple[int, int, int, int], tuple[int, int, int, int]]]:
        return list(zip(self.in_boxes, self.out_boxes))


def zip_extract_file(zip_file: ZipFile, entry_name: str, out_path: Path):
    logger.info("Extracting %s to %s", entry_name, out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with (
        zip_file.open(entry_name, "r") as entry,
        out_path.open("wb") as out_file,
    ):
        shutil.copyfileobj(entry, out_file)


def zip_extract_files(zip_file: ZipFile, entry_names: list[tuple[str, Path]]):
    for entry_name, out_path in entry_names:
        zip_extract_file(zip_file, entry_name, out_path)


def image_generate_nine_patch(
    in_image: Image.Image, out_image_path: Path, nine_patch: NinePatch
):
    logger.info("Generating nine-patch image %s", out_image_path)

    out_image = Image.new("RGBA", nine_patch.out_size, (0, 0, 0, 0))
    for box_in, box_out in nine_patch.boxes:
        logger.debug("Cropping %s and pasting to %s", box_in, box_out)
        patch = in_image.crop(box_in)
        out_image.paste(patch, box_out)

    out_image_path.parent.mkdir(parents=True, exist_ok=True)
    out_image.save(out_image_path)


def image_generate_nine_patches(
    zip_file: ZipFile, entry_name: str, out_: list[tuple[Path, NinePatch]]
) -> None:
    in_image = Image.open(zip_file.open(entry_name, "r")).convert("RGBA")
    for out_image_path, nine_patch in out_:
        image_generate_nine_patch(in_image, out_image_path, nine_patch)


def extract_sprout_ui(sprout_ui_zip: Path, assets_dir: Path, clean: bool = False):
    sprout_ui_dir = assets_dir / "sprout" / "ui"
    if clean:
        shutil.rmtree(sprout_ui_dir, ignore_errors=True)
    sprout_ui_dir.mkdir(parents=True, exist_ok=True)
    logger.info(
        "Extracting Sprout UI assets from %s to %s", sprout_ui_zip, sprout_ui_dir
    )

    with ZipFile(sprout_ui_zip, "r") as zip_file:
        zip_extract_files(
            zip_file,
            [
                (
                    "Sprout Lands - UI Pack - Basic pack/fonts/pixelFont-7-8x14-sproutLands.ttf",
                    sprout_ui_dir / "fonts" / "font_8x14.ttf",
                ),
                (
                    "Sprout Lands - UI Pack - Basic pack/fonts/pixel-letters-7-8x14.png",
                    sprout_ui_dir / "fonts" / "font_8x14.png",
                ),
            ],
        )

        image_generate_nine_patches(
            zip_file,
            "Sprout Lands - UI Pack - Basic pack/Sprite sheets/Sprite sheet for Basic Pack.png",
            [
                (
                    sprout_ui_dir / "dialogs" / "wood_frame" / f"{color}_{style}.png",
                    NinePatch(
                        8,
                        8,
                        8,
                        8,
                        16,
                        16,
                        in_offset_x=152 + i_style * 48,
                        in_offset_y=8 + i_color * 48,
                    ),
                )
                for (i_color, color), (i_style, style) in product(
                    enumerate(
                        ["light", "medium", "dark"],
                    ),
                    enumerate(["plain", "nailed"]),
                )
            ],
        )


def main(args: Iterable[str] | None = None) -> None:

    parser = ArgumentParser(description="Extract assets from a game.")
    parser.add_argument(
        "-l",
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).",
    )
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
        default=ASSETS_DIR,
        help="Directory in which to extract the assets.",
    )
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="Clean the assets directory before extracting.",
    )
    parsed_args = parser.parse_args(args)
    logging.basicConfig(
        level=getattr(logging, parsed_args.log_level),
        format="%(levelname)s: %(message)s",
    )

    extract_sprout_ui(
        parsed_args.sprout_ui, parsed_args.assets_dir, clean=parsed_args.clean
    )


if __name__ == "__main__":
    main()
