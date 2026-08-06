import importlib
import pkgutil
from argparse import ArgumentParser
from collections.abc import Iterable

from dotenv import load_dotenv

from lapinou import commands as commands_module
from lapinou.core.command import BaseCommand


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
