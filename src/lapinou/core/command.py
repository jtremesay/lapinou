from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace


class BaseCommand(ABC):
    help_text = None

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add command arguments to the parser."""

    @abstractmethod
    def handle(self, args: Namespace) -> None:
        """Handle the command logic."""
        ...
