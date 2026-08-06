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

from lapinou.ge.director import Director
from lapinou.ge.scene import Scene


class Scene02(Scene):
    def update(self, dt: float, director: Director, screen: Surface) -> None:
        screen.fill("green")

        keys = pg.key.get_just_released()
        if keys[pg.K_SPACE]:
            director.pop_scene()
