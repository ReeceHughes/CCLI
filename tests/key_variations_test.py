import pytest

from ccli import CCLI, Command
from tests.command_mock import CommandMock


class BadKey1(Command):
    key = 1


class TestBadKey1(CommandMock):
    uses_commands = [BadKey1]

    def test_bad_key(self):
        with pytest.raises(NotImplementedError):
            CCLI()


# Instance methods are not supported.
# Key must be known before instantiation
class BadKey2(Command):
    def key(self):
        return "function"


class TestBadKey2(CommandMock):
    uses_commands = [BadKey2]

    def test_bad_key(self):
        with pytest.raises(NotImplementedError):
            CCLI()


class TestBadKey3(CommandMock):
    uses_commands = [BadKey2]

    def test_bad_key(self):
        with pytest.raises(NotImplementedError):
            CCLI()


class ClassKey(Command):
    key = "class"

    # Instance methods as keys are not supported.
    # Because an alt_key is not required, no error will be thrown.
    def alt_key(self):
        return "alt class"


class ClassmethodKey(Command):
    @classmethod
    def key(cls):
        return "classmethod"

    @classmethod
    def short_key(cls):
        return "cm"


class StaticmethodKey(Command):
    @staticmethod
    def key():
        return "static"

    @staticmethod
    def alt_key():
        return "static-method"


class TestOkayKey(CommandMock):
    uses_commands = [ClassKey, ClassmethodKey, StaticmethodKey]

    def test_okay_key(self):
        CCLI()
