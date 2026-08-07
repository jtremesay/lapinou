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
from typing import Any

from arcade import Window
from arcade import run as arcade_run

from lapinou.core.command import BaseCommand

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
        # Load the game entry point module
        try:
            entry_point = import_module(f"{args.game}.entrypoint")
        except ModuleNotFoundError:
            logger.exception("Error: The game '%s' could not be found.", args.game)
            return

        # Load the entry point scene from the game module
        try:
            get_entry_view: Any = entry_point.get_entry_view
        except AttributeError:
            logger.error(
                "Error: The game '%s' does not have a 'get_entry_view' function.",
                args.game,
            )
            return

        # Create the window and run the game
        window = Window(1280, 720, args.game)
        window.show_view(get_entry_view())
        arcade_run()
