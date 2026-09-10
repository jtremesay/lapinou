from argparse import ArgumentParser
from collections.abc import Iterable
from itertools import batched, product
from pathlib import Path

import arcade

DATA_DIR = Path("thirds/pokered")

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


class MapViewer(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Map Viewer")
        self.camera_sprites = arcade.Camera2D(zoom=2)

    def setup(self):
        map_name = "RedsHouse2F"
        tileset_name = "reds_house"
        map_width = 4
        map_height = 4
        self.camera_sprites.position = arcade.Vec2(0, 0)

        tileset_path = DATA_DIR / "gfx/tilesets" / f"{tileset_name}.png"
        block_sets_path = DATA_DIR / f"gfx/blocksets/{tileset_name}.bst"
        map_path = DATA_DIR / f"maps/{map_name}.blk"
        self.bg_tiles = arcade.SpriteList()

        block_sets = tuple(batched(block_sets_path.read_bytes(), 4 * 4))
        tiles_spritesheet = arcade.load_spritesheet(tileset_path)
        textures = {
            (x, y): tiles_spritesheet.get_texture(
                arcade.XYWH(x * 8, y * 8, 8, 8, arcade.Vec2(0, 0))
            )
            for x, y in product(range(16), range(tiles_spritesheet.image.height // 8))
        }

        for block_i, block_idx in enumerate(map_path.read_bytes()):
            block_x = block_i % map_width
            block_y = block_i // map_width
            print(
                f"block_i={block_i}, block_idx={block_idx}, block_x={block_x}, block_y={block_y}"
            )
            block = block_sets[block_idx]
            for tile_i, tile_idx in enumerate(block):
                tile_x = tile_idx % 16
                tile_y = tile_idx // 16
                tile = textures[(tile_x, tile_y)]

                sprite_x = (block_x * 4 + (tile_i % 4)) * 8 + 4
                sprite_y = (map_height - 1 - (block_y * 4 + (tile_i // 4))) * 8 + 4
                print(f"sprite_x={sprite_x}, sprite_y={sprite_y}")

                sprite = arcade.Sprite(
                    tile,
                    center_x=sprite_x,
                    center_y=sprite_y,
                )
                self.bg_tiles.append(sprite)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.camera_sprites.position += arcade.Vec2(0, 10)
        elif symbol == arcade.key.DOWN:
            self.camera_sprites.position += arcade.Vec2(0, -10)
        elif symbol == arcade.key.LEFT:
            self.camera_sprites.position += arcade.Vec2(-10, 0)
        elif symbol == arcade.key.RIGHT:
            self.camera_sprites.position += arcade.Vec2(10, 0)

    def on_mouse_scroll(self, x: float, y: float, scroll_x: float, scroll_y: float):
        self.camera_sprites.zoom += scroll_y * 0.1

    def on_draw(self):
        self.clear()
        self.camera_sprites.use()
        self.bg_tiles.draw()


def main(args: Iterable[str] | None = None):
    parser = ArgumentParser()
    _parsed_args = parser.parse_args(args)

    viewer = MapViewer()
    viewer.setup()
    arcade.run()
