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

from pygame import Surface
from pygame import image as pgi
from pygame.sprite import Group
from pygame.typing import IntPoint

from lapinou.sprites.ninepatch import NinePatch
from lapinou.sprites.ninepatch_sprite import NinePatchSprite

from ..assets import SPROUT_UI_DIR


class WoodFrameSprite(NinePatchSprite):
    class Color(StrEnum):
        LIGHT = "light"
        MEDIUM = "medium"
        DARK = "dark"

    class Style(StrEnum):
        PLAIN = "plain"
        NAILED = "nailed"

    def __init__(
        self,
        color: Color,
        style: Style,
        *groups: Group,
        center_size: IntPoint | None = None,
    ):
        super().__init__(
            self.image_from_color_and_style(color, style),
            NinePatch((8, 8, 8, 8)),
            *groups,
            center_size=center_size,
        )

    @classmethod
    def image_path_from_color_and_style(cls, color: Color, style: Style) -> Path:
        return (
            SPROUT_UI_DIR
            / "dialogs"
            / "wood_frame"
            / f"{color.value}_{style.value}.png"
        )

    @classmethod
    def image_from_color_and_style(cls, color: Color, style: Style) -> Surface:
        return pgi.load(cls.image_path_from_color_and_style(color, style))
