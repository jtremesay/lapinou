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
from argparse import ArgumentParser, Namespace

import pygame

from lapinou.core.command import BaseCommand
from lapinou.game.scenes.main_menu import MainMenuScene
from lapinou.ge.director import Director


class Command(BaseCommand):
    help_text = "Start lapinou"

    def add_arguments(self, parser: ArgumentParser) -> None:
        pass

    def handle(self, args: Namespace) -> None:
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))

        director = Director(MainMenuScene())
        director.run(screen)

        pygame.quit()
