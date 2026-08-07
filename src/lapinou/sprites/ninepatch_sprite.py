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
from pygame import SRCALPHA, Rect, Surface
from pygame import transform as pgt
from pygame.sprite import Group, Sprite
from pygame.typing import IntPoint

from .ninepatch import NinePatch


def patch_sprites(
    nine_patch: NinePatch, image: Surface, *groups: Group
) -> list[Sprite]:
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
        *groups: Group,
        center_size: IntPoint | None = None,
    ):
        super().__init__(*groups)
        self._source_image = image
        self._pre_rendered_image: Surface | None = None
        self.nine_patch = nine_patch

        self.rect = Rect(0, 0, self.nine_patch.width, self.nine_patch.height)
        self._center_size = (0, 0)
        self.center_size = center_size if center_size is not None else self._center_size

    @property
    def center_size(self) -> IntPoint:
        return self._center_size

    @center_size.setter
    def center_size(self, value: IntPoint):
        self._center_size = value
        self.rect.width = float(
            self.nine_patch.outer_size[0]
            + self._center_size[0]
            + self.nine_patch.outer_size[2]
        )
        self.rect.height = float(
            self.nine_patch.outer_size[1]
            + self._center_size[1]
            + self.nine_patch.outer_size[3]
        )
        self._image = None

    @property
    def image(self) -> Surface:
        if self._pre_rendered_image is None:
            rects: list[tuple[Surface, Rect]] = [
                # Top left corner
                (
                    self._source_image.subsurface(
                        0,
                        0,
                        self.nine_patch.outer_size[0],
                        self.nine_patch.outer_size[1],
                    ),
                    Rect(
                        0,
                        0,
                        self.nine_patch.outer_size[0],
                        self.nine_patch.outer_size[1],
                    ),
                ),
                # Top edge
                (
                    pgt.scale_by(
                        self._source_image.subsurface(
                            self.nine_patch.outer_size[0],
                            0,
                            self.nine_patch.center_size[0],
                            self.nine_patch.outer_size[1],
                        ),
                        (self._center_size[0], 1),
                    ),
                    Rect(
                        self.nine_patch.outer_size[0],
                        0,
                        self._center_size[0],
                        self.nine_patch.outer_size[1],
                    ),
                ),
                # Top right corner
                (
                    self._source_image.subsurface(
                        self.nine_patch.outer_size[0] + self.nine_patch.center_size[0],
                        0,
                        self.nine_patch.outer_size[2],
                        self.nine_patch.outer_size[1],
                    ),
                    Rect(
                        self.nine_patch.outer_size[0] + self._center_size[0],
                        0,
                        self.nine_patch.outer_size[2],
                        self.nine_patch.outer_size[1],
                    ),
                ),
                # Left edge
                (
                    pgt.scale_by(
                        self._source_image.subsurface(
                            0,
                            self.nine_patch.outer_size[1],
                            self.nine_patch.outer_size[0],
                            self.nine_patch.center_size[1],
                        ),
                        (1, self._center_size[1]),
                    ),
                    Rect(
                        0,
                        self.nine_patch.outer_size[1],
                        self.nine_patch.outer_size[0],
                        self._center_size[1],
                    ),
                ),
                # Center
                (
                    pgt.scale_by(
                        self._source_image.subsurface(
                            self.nine_patch.outer_size[0],
                            self.nine_patch.outer_size[1],
                            self.nine_patch.center_size[0],
                            self.nine_patch.center_size[1],
                        ),
                        self._center_size,
                    ),
                    Rect(
                        self.nine_patch.outer_size[0],
                        self.nine_patch.outer_size[1],
                        self._center_size[0],
                        self._center_size[1],
                    ),
                ),
                # Right edge
                (
                    pgt.scale_by(
                        self._source_image.subsurface(
                            self.nine_patch.outer_size[0]
                            + self.nine_patch.center_size[0],
                            self.nine_patch.outer_size[1],
                            self.nine_patch.outer_size[2],
                            self.nine_patch.center_size[1],
                        ),
                        (1, self._center_size[1]),
                    ),
                    Rect(
                        self.nine_patch.outer_size[0] + self._center_size[0],
                        self.nine_patch.outer_size[1],
                        self.nine_patch.outer_size[2],
                        self._center_size[1],
                    ),
                ),
                # Bottom left corner
                (
                    self._source_image.subsurface(
                        0,
                        self.nine_patch.outer_size[1] + self.nine_patch.center_size[1],
                        self.nine_patch.outer_size[0],
                        self.nine_patch.outer_size[3],
                    ),
                    Rect(
                        0,
                        self.nine_patch.outer_size[1] + self._center_size[1],
                        self.nine_patch.outer_size[0],
                        self.nine_patch.outer_size[3],
                    ),
                ),
                # Bottom edge
                (
                    pgt.scale_by(
                        self._source_image.subsurface(
                            self.nine_patch.outer_size[0],
                            self.nine_patch.outer_size[1]
                            + self.nine_patch.center_size[1],
                            self.nine_patch.center_size[0],
                            self.nine_patch.outer_size[3],
                        ),
                        (self._center_size[0], 1),
                    ),
                    Rect(
                        self.nine_patch.outer_size[0],
                        self.nine_patch.outer_size[1] + self._center_size[1],
                        self._center_size[0],
                        self.nine_patch.outer_size[3],
                    ),
                ),
                # Bottom right corner
                (
                    self._source_image.subsurface(
                        self.nine_patch.outer_size[0] + self.nine_patch.center_size[0],
                        self.nine_patch.outer_size[1] + self.nine_patch.center_size[1],
                        self.nine_patch.outer_size[2],
                        self.nine_patch.outer_size[3],
                    ),
                    Rect(
                        self.nine_patch.outer_size[0] + self._center_size[0],
                        self.nine_patch.outer_size[1] + self._center_size[1],
                        self.nine_patch.outer_size[2],
                        self.nine_patch.outer_size[3],
                    ),
                ),
            ]

            image = Surface(self.rect.size, flags=SRCALPHA)
            image.blits(rects)
            image = pgt.scale_by(image, 4)

            self._pre_rendered_image = image

        return self._pre_rendered_image
