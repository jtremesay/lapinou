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
from pathlib import Path

from ..agents import create_agent, create_character
from ..core.command import BaseCommand


class Command(BaseCommand):
    help_text = "Character generator"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "-s", "--save", type=Path, help="Save the generated character to a file"
        )

    def handle(self, args: Namespace) -> None:
        agent = create_agent()
        character = create_character(agent)
        print(character)

        if args.save:
            with open(args.save, "w") as f:
                f.write(character.model_dump_json(indent=4))
            print(f"Character saved to {args.save}")
