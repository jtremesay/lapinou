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
from importlib import import_module
from logging import getLogger
from os import getenv

import pygame

from ..core.command import BaseCommand
from ..director import Director

logger = getLogger(__name__)


class Command(BaseCommand):
    help_text = "Run a game"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "-g",
            "--game",
            default=getenv("LAPINOU_GAME", "llmrpg"),
            type=str,
            help="The game to run (e.g., 'my_game')",
        )

    def handle(self, args: Namespace) -> None:
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))
        try:
            entry_point = import_module(f"{args.game}.entrypoint")
        except ModuleNotFoundError:
            logger.error("Error: The game '%s' could not be found.", args.game)
            return
        try:
            get_entrypoint_scene = entry_point.get_entrypoint_scene
        except AttributeError:
            logger.error(
                "Error: The game '%s' does not have a 'get_entrypoint_scene' function.",
                args.game,
            )
            return

        director = Director(get_entrypoint_scene())
        director.run(screen)

        pygame.quit()
