from argparse import ArgumentParser, Namespace

from lapinou.core.command import BaseCommand


class Command(BaseCommand):
    help_text = "Start lapinou"

    def add_arguments(self, parser: ArgumentParser) -> None:
        pass

    def handle(self, args: Namespace) -> None:
        pass
