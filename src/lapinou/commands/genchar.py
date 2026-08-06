from argparse import ArgumentParser, Namespace
from pathlib import Path

from lapinou.agents import create_agent, create_character
from lapinou.core.command import BaseCommand


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
