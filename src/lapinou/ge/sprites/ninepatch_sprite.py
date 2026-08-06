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

from pygame import Rect, Surface
from pygame.sprite import Group, Sprite
from pygame.typing import IntPoint

from .ninepatch import NinePatch


def patch_sprites(nine_patch: NinePatch, image: Surface, *groups) -> list[Sprite]:
    sprites = []
    for box in nine_patch.boxes:
        sprite = Sprite(*groups)
        sprite.image = image.subsurface(box)
        sprites.append(sprite)

    return sprites


class NinePatchSprite(Sprite):
    def __init__(
        self,
        image: Surface,
        nine_patch: NinePatch,
        center_size: IntPoint | None = None,
        *groups: Group,
    ):
        super().__init__(*groups)
        # self.image = image
        self.nine_patch = nine_patch

        (
            self.top_left,
            self.top,
            self.top_right,
            self.left,
            self.center,
            self.right,
            self.bottom_left,
            self.bottom,
            self.bottom_right,
        ) = patch_sprites(self.nine_patch, image, self)

        self.rect = Rect(0, 0, self.nine_patch.width, self.nine_patch.height)
        self._center_size = (0, 0)
        self.center_size = center_size if center_size is not None else self._center_size

    @property
    def center_size(self) -> IntPoint:
        return self._center_size

    @center_size.setter
    def center_size(self, value: IntPoint):
        self._center_size = value
        self.top_left.rect = Rect(
            0, 0, self.nine_patch.outer_size.left, self.nine_patch.outer_size.top
        )
        self.top.rect = Rect(
            self.nine_patch.outer_size.left,
            0,
            self._center_size[0],
            self.nine_patch.outer_size.top,
        )
        self.top_right.rect = Rect(
            self.nine_patch.outer_size.left + self._center_size[0],
            0,
            self.nine_patch.outer_size.right,
            self.nine_patch.outer_size.top,
        )
        self.left.rect = Rect(
            0,
            self.nine_patch.outer_size.top,
            self.nine_patch.outer_size.left,
            self._center_size[1],
        )
        self.center.rect = Rect(
            self.nine_patch.outer_size.left,
            self.nine_patch.outer_size.top,
            self._center_size[0],
            self._center_size[1],
        )
        self.right.rect = Rect(
            self.nine_patch.outer_size.left + self._center_size[0],
            self.nine_patch.outer_size.top,
            self.nine_patch.outer_size.right,
            self._center_size[1],
        )
        self.bottom_left.rect = Rect(
            0,
            self.nine_patch.outer_size.top + self._center_size[1],
            self.nine_patch.outer_size.left,
            self.nine_patch.outer_size.bottom,
        )
        self.bottom.rect = Rect(
            self.nine_patch.outer_size.left,
            self.nine_patch.outer_size.top + self._center_size[1],
            self._center_size[0],
            self.nine_patch.outer_size.bottom,
        )
        self.bottom_right.rect = Rect(
            self.nine_patch.outer_size.left + self._center_size[0],
            self.nine_patch.outer_size.top + self._center_size[1],
            self.nine_patch.outer_size.right,
            self.nine_patch.outer_size.bottom,
        )

        self.rect.width = float(
            self.nine_patch.outer_size.left
            + self._center_size[0]
            + self.nine_patch.outer_size.right
        )
        self.rect.height = float(
            self.nine_patch.outer_size.top
            + self._center_size[1]
            + self.nine_patch.outer_size.bottom
        )
