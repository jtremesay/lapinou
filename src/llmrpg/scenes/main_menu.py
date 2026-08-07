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
from pygame import Surface
from pygame.sprite import Group

from lapinou.director import Director
from lapinou.scene import Scene

from ..sprites.wood_frame import WoodFrameSprite


class MainMenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.root_group = Group()
        self.frame = WoodFrameSprite(
            WoodFrameSprite.Color.DARK,
            WoodFrameSprite.Style.NAILED,
            self.root_group,
            center_size=(100, 100),
        )
        self.frame.rect.center = (400, 300)

    def update(self, dt: float, director: Director) -> None:
        self.root_group.update(dt)

    def draw(self, screen: Surface) -> None:
        screen.fill("green")
        self.root_group.draw(screen)
