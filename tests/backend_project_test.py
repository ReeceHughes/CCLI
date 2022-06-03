import pytest

from ccli import CCLI
from tests.command_mock import CommandMock
from tests.backend_project_commands import (
    StartServer,
    SeedDatabase,
    UnitTest,
    CleanDatabase,
)


def make_cli(args):
    return CCLI(name="Backend Project", cli_args=["ccli"] + args)


class TestBackendProject(CommandMock):
    uses_commands = [StartServer, SeedDatabase, UnitTest, CleanDatabase]

    @staticmethod
    @pytest.fixture(autouse=True)
    def reset_run_count():
        yield
        StartServer.run_count = 0
        SeedDatabase.run_count = 0
        UnitTest.run_count = 0
        CleanDatabase.run_count = 0

    @staticmethod
    def assert_run_counts(start_count=0, seed_count=0, test_count=0, clean_count=0):
        assert StartServer.run_count == start_count
        assert SeedDatabase.run_count == seed_count
        assert UnitTest.run_count == test_count
        assert CleanDatabase.run_count == clean_count

    def test_one_command(self):
        c = make_cli(["start"])
        assert len(c.args) == 2
        self.assert_run_counts(start_count=1)

    def test_one_command_with_args(self):
        c = make_cli(["start", "--debug"])
        self.assert_run_counts(start_count=1)

        assert c.invoked_commands[0].instance.args.debug is True

    def test_two_commands(self):
        c = make_cli(["test", "s"])
        self.assert_run_counts(start_count=1, test_count=1)

        # Test
        assert c.invoked_commands[0].instance.args.debug is False
        assert c.invoked_commands[0].instance.args.cov is True
        # Start
        assert c.invoked_commands[1].instance.args.debug is False

    def test_two_commands_with_args(self):
        c = make_cli(["seed", "./file.sql", "start", "--port", "5432"])
        self.assert_run_counts(start_count=1, seed_count=1)

        # Seed
        assert c.invoked_commands[0].instance.args.sql_file == ["./file.sql"]
        # Start
        assert c.invoked_commands[1].instance.args.debug is False
        assert c.invoked_commands[1].instance.args.port == 5432

    def test_skip_command(self):
        # Seed SQL file is called test
        c = make_cli(
            ["seed-db", "--cli-skip-command", "test", "start", "--port", "5432"]
        )
        self.assert_run_counts(start_count=1, seed_count=1)

        # Seed
        assert c.invoked_commands[0].instance.args.sql_file == ["test"]
        # Start
        assert c.invoked_commands[1].instance.args.debug is False
        assert c.invoked_commands[1].instance.args.port == 5432

    def test_default_parser(self):
        make_cli(["clean-db"])
        self.assert_run_counts(clean_count=1)

    def test_no_chaining(self):
        cli = CCLI(
            name="Backend Project",
            enable_chaining=False,
            cli_args=["ccli", "seed", "./file.sql", "start", "test"],
        )

        self.assert_run_counts(seed_count=1)

        assert len(cli.invoked_commands) == 1
        assert cli.invoked_commands[0].instance.args.sql_file == [
            "./file.sql",
            "start",
            "test",
        ]

    def test_default_reprs(self):
        cli = make_cli(["s", "-d"])

        assert str(SeedDatabase(["file"])) == "Command(key=seed, args=['file'])"
        assert (
            str(cli.invoked_commands[0])
            == "InvokedCommand(key=s, type=StartServer, args=Namespace(debug=True, port=None))"
        )
