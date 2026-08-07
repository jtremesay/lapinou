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

from dataclasses import dataclass, field

from pygame import Rect
from pygame.typing import IntPoint


@dataclass
class NinePatch:
    outer_size: tuple[int, int, int, int]  # Widths of left, top, right and bottom
    center_size: tuple[int, int] = field(
        default_factory=lambda: (1, 1)
    )  # width and height of the center patch

    @property
    def width(self) -> int:
        return self.outer_size[0] + self.center_size[0] + self.outer_size[2]

    @property
    def height(self) -> int:
        return self.outer_size[1] + self.center_size[1] + self.outer_size[3]

    @property
    def size(self) -> IntPoint:
        return (self.width, self.height)

    @property
    def top_left_box(self) -> Rect:
        return Rect(0, 0, self.outer_size[0], self.outer_size[1])

    @property
    def top_box(self) -> Rect:
        return Rect(self.outer_size[0], 0, self.center_size[0], self.outer_size[1])

    @property
    def top_right_box(self) -> Rect:
        return Rect(
            self.outer_size[0] + self.center_size[0],
            0,
            self.outer_size[2],
            self.outer_size[1],
        )

    @property
    def left_box(self) -> Rect:
        return Rect(0, self.outer_size[1], self.outer_size[0], self.center_size[1])

    @property
    def center_box(self) -> Rect:
        return Rect(
            self.outer_size[0],
            self.outer_size[1],
            self.center_size[0],
            self.center_size[1],
        )

    @property
    def right_box(self) -> Rect:
        return Rect(
            self.outer_size[0] + self.center_size[0],
            self.outer_size[1],
            self.outer_size[2],
            self.center_size[1],
        )

    @property
    def bottom_left_box(self) -> Rect:
        return Rect(
            0,
            self.outer_size[1] + self.center_size[1],
            self.outer_size[0],
            self.outer_size[3],
        )

    @property
    def bottom_box(self) -> Rect:
        return Rect(
            self.outer_size[0],
            self.outer_size[1] + self.center_size[1],
            self.center_size[0],
            self.outer_size[3],
        )

    @property
    def bottom_right_box(self) -> Rect:
        return Rect(
            self.outer_size[0] + self.center_size[0],
            self.outer_size[1] + self.center_size[1],
            self.outer_size[2],
            self.outer_size[3],
        )

    @property
    def boxes(self) -> list[Rect]:
        return [
            self.top_left_box,
            self.top_box,
            self.top_right_box,
            self.left_box,
            self.center_box,
            self.right_box,
            self.bottom_left_box,
            self.bottom_box,
            self.bottom_right_box,
        ]
