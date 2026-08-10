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
from logging import getLogger
from pathlib import Path

from arcade import Window
from arcade import run as arcade_run

from lapinou.core.command import BaseCommand
from lapinou.models.settings import Settings
from lapinou.views.main_menu import MainMenuView

logger = getLogger(__name__)


class Command(BaseCommand):
    help_text = "Run a game"

    def add_arguments(self, parser: ArgumentParser) -> None: ...

    def handle(self, args: Namespace) -> None:
        settings_path = Path("settings.json")
        try:
            settings = Settings.load_from_file(settings_path)
        except FileNotFoundError:
            settings = None

        # Create the window and run the game
        window = Window(1280, 720, title="Lapinou - An agentic game engine")
        window.show_view(MainMenuView(settings=settings))
        arcade_run()
