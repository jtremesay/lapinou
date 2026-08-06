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


import pygame as pg
from pygame import Surface
from pygame.time import Clock

from .scene import Scene


class Director:
    def __init__(self, root: Scene | None = None):
        self.scenes = [root] if root is not None else []

    def top_scene(self) -> Scene | None:
        try:
            return self.scenes[-1]
        except IndexError:
            return None

    def push_scene(self, scene: Scene) -> None:
        self.scenes.append(scene)

    def pop_scene(self) -> Scene | None:
        try:
            return self.scenes.pop()
        except IndexError:
            return None

    def replace_scene(self, scene: Scene) -> None:
        try:
            self.scenes[-1] = scene
        except IndexError:
            self.scenes.append(scene)

    def update(self, dt: float, screen: Surface) -> None:
        if scene := self.top_scene():
            scene.update(dt, self, screen)

    def run(self, screen: Surface) -> None:
        clock = Clock()
        target_fps = 60
        dt = 1 / target_fps  # Run the game at virtual 60 updates per second
        while self.scenes:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    return

            self.update(dt, screen)

            pg.display.flip()
            clock.tick(target_fps)
