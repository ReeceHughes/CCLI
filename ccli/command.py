"""Cirkit Digital
"""

from argparse import ArgumentParser
from abc import ABC, abstractmethod


class Command(ABC):
    """Base class for commands runnable from the CCLI.

    A key (how the command is invoked) must be defined.

        from ccli import Command

        class StartServer(Command):
            key = "start"
            short_key = "s"

            def run(self):
                print('Starting the server')
    """

    parser = None

    @classmethod
    @abstractmethod
    def key(cls) -> str:
        """Invocation key for the command."""

    @classmethod
    def short_key(cls) -> str:
        """Short version of `key`."""

    @classmethod
    def alt_key(cls) -> str:
        """Alternative invocation key."""

    def __init__(self, args):
        """Creates a runnable command.

        Args:
            args: List of arguments given to this command.
        """
        self.args = args

    def run(self):
        """Runs the command.

        Called from the CCLI when the command invoked.
        """

    def __repr__(self):
        return "Command(key=%s, args=%s)" % (self.key, self.args)

    @classmethod
    def parse(cls, args_list):
        """Default argument parser.

        This may be overridden to provide a different argument parser.
        """
        # If the user chose not to implement their own parser/args, use a default parser.
        if cls.parser is None:
            cls.parser = ArgumentParser(prog=str(cls.key))
        return cls.parser.parse_args(args_list)
