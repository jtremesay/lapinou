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
import importlib
import pkgutil
from argparse import ArgumentParser
from collections.abc import Iterable

from dotenv import load_dotenv

from lapinou import commands as commands_module

from .command import BaseCommand


def main(args: Iterable[str] | None = None) -> None:
    load_dotenv()  # Load environment variables from .env file

    parser = ArgumentParser(description="Lapinou CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Autodiscovers the commands modules and use ther Command class to add the subparser
    for _, module_name, _ in pkgutil.iter_modules(commands_module.__path__):
        module = importlib.import_module(f"{commands_module.__name__}.{module_name}")
        if (Command := getattr(module, "Command", None)) is not None and issubclass(
            Command, BaseCommand
        ):
            command_instance = Command()
            subparser = subparsers.add_parser(
                module_name, help=command_instance.help_text
            )
            command_instance.add_arguments(subparser)
            subparser.set_defaults(command=command_instance.handle)

    parsed_args = parser.parse_args(args)
    if (func := getattr(parsed_args, "command", None)) is not None:
        func(parsed_args)
    else:
        parser.print_help()
