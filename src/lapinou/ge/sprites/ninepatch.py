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

from dataclasses import dataclass

from pygame import Rect
from pygame.typing import IntPoint


@dataclass
class NinePatch:
    outer_size: Rect  # Width and height of left, top, right and bottom
    center_size: IntPoint  # width and height of the center patch

    @property
    def width(self) -> int:
        return self.outer_size.left + self.center_size[0] + self.outer_size.right

    @property
    def height(self) -> int:
        return self.outer_size.top + self.center_size[1] + self.outer_size.bottom

    @property
    def size(self) -> IntPoint:
        return (self.width, self.height)

    @property
    def top_left_box(self) -> Rect:
        return Rect(0, 0, self.outer_size.left, self.outer_size.top)

    @property
    def top_box(self) -> Rect:
        return Rect(self.outer_size.left, 0, self.center_size[0], self.outer_size.top)

    @property
    def top_right_box(self) -> Rect:
        return Rect(
            self.outer_size.left + self.center_size[0],
            0,
            self.outer_size.right,
            self.outer_size.top,
        )

    @property
    def left_box(self) -> Rect:
        return Rect(0, self.outer_size.top, self.outer_size.left, self.center_size[1])

    @property
    def center_box(self) -> Rect:
        return Rect(
            self.outer_size.left,
            self.outer_size.top,
            self.center_size[0],
            self.center_size[1],
        )

    @property
    def right_box(self) -> Rect:
        return Rect(
            self.outer_size.left + self.center_size[0],
            self.outer_size.top,
            self.outer_size.right,
            self.center_size[1],
        )

    @property
    def bottom_left_box(self) -> Rect:
        return Rect(
            0,
            self.outer_size.top + self.center_size[1],
            self.outer_size.left,
            self.outer_size.bottom,
        )

    @property
    def bottom_box(self) -> Rect:
        return Rect(
            self.outer_size.left,
            self.outer_size.top + self.center_size[1],
            self.center_size[0],
            self.outer_size.bottom,
        )

    @property
    def bottom_right_box(self) -> Rect:
        return Rect(
            self.outer_size.left + self.center_size[0],
            self.outer_size.top + self.center_size[1],
            self.outer_size.right,
            self.outer_size.bottom,
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
