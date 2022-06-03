from unittest.mock import MagicMock

from ccli import Command


class CommandMock:
    @classmethod
    def setup_class(cls):
        commands = cls.__dict__.get("uses_commands")
        if commands is not None:
            c = Command
            c.__subclasses__ = MagicMock(return_value=commands)
