# Lapinou - An agentic game engine
# Copyright (C) 2026 Jonathan Tremesaygues
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from enum import StrEnum
from pathlib import Path

from arcade import load_texture
from arcade.gui import NinePatchTexture, UIWidget

from lapinou.assets import SPROUT_UI_DIR


class WoodFrameColor(StrEnum):
    LIGHT = "light"
    MEDIUM = "medium"
    DARK = "dark"


class WoodFramePattern(StrEnum):
    PLAIN = "plain"
    NAILED = "nailed"


def wood_frame_image_path(color: WoodFrameColor, pattern: WoodFramePattern) -> Path:
    return (
        SPROUT_UI_DIR / "dialogs" / "wood_frame" / f"{color.value}_{pattern.value}.png"
    )


def wood_frame_texture(
    color: WoodFrameColor = WoodFrameColor.LIGHT,
    pattern: WoodFramePattern = WoodFramePattern.PLAIN,
) -> NinePatchTexture:
    return NinePatchTexture(
        8,
        8,
        8,
        8,
        load_texture(wood_frame_image_path(color, pattern)),
    )


def with_wood_frame_background(
    widget: UIWidget,
    color: WoodFrameColor = WoodFrameColor.LIGHT,
    pattern: WoodFramePattern = WoodFramePattern.PLAIN,
) -> UIWidget:
    """Add a wood frame background to a widget."""
    return widget.with_background(
        texture=wood_frame_texture(color, pattern)
    ).with_padding(top=20, right=20, bottom=20, left=20)
