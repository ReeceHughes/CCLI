from argparse import ArgumentParser

from ccli import CCLI, Command
from tests.command_mock import CommandMock


class SubCommand:
    def __init__(self, args):
        self.args = args
        self.run_count = 0

    def run(self):
        self.run_count += 1


class SubSubCommand(SubCommand, Command):
    key = "sub"
    parser = ArgumentParser(prog="Mixin")


class TestSubCommand(CommandMock):
    uses_commands = [SubSubCommand]

    def test_call_both(self):
        args = ["cli.py", "sub"]
        c = CCLI(cli_args=args)
        assert len(c.available_commands) == 1
        assert len(c.invoked_commands) == 1
        assert c.invoked_commands[0].instance.run_count == 1
