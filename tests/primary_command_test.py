from ccli import CCLI
from tests.command_mock import CommandMock
from tests.backend_project_commands import StartServer, Primary


class TestPrimaryCommand(CommandMock):
    uses_commands = [Primary, StartServer]

    def test_primary(self):
        args = ["r", "-e", ".env", "start"]
        c = CCLI(primary_command_class=Primary, cli_args=args)
        assert Primary.run_count == 1
        assert StartServer.run_count == 1
        assert c.invoked_commands[0].instance.args.env == ".env"
