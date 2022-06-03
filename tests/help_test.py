import subprocess
from os import environ


class TestHelpText:
    """
    Argparse calls system.exit after displaying help text.
    Run the cli in a different process to not exit the tests.
    """

    cli_name = "Help Text Test"
    first_line_idx = 0

    def test_help_text_with_primary(self):
        output = self._run_script("./tests/backend_project_commands.py")

        avail_commands = "{start,s,seed,seed-db,test,clean-db}"
        primary_command_desc_idx = self.first_line_idx + 2
        avail_commands_idx = primary_command_desc_idx + 3
        # Available command list index + 4 available commands + 4 filler lines
        primary_command_args_idx = avail_commands_idx + 4 + 4

        assert self.cli_name in output[self.first_line_idx]
        assert "Primary command" in output[primary_command_desc_idx]
        assert avail_commands in output[self.first_line_idx]
        assert avail_commands in output[avail_commands_idx]

        assert "Start the server" in output[avail_commands_idx + 2]
        assert "Seed the database" in output[avail_commands_idx + 3]
        assert "Run unit tests" in output[avail_commands_idx + 4]
        assert "Run clean-db -h for more information" in output[avail_commands_idx + 5]

        assert "-h, --help" in output[primary_command_args_idx]
        assert "-e ENV, --env ENV" in output[primary_command_args_idx + 1]
        assert "Primary CLI Environment" in output[primary_command_args_idx + 1]

    def test_help_text_no_primary(self):
        output = self._run_script("./tests/cli_no_primary.py")

        assert self.cli_name in output[self.first_line_idx]

    @staticmethod
    def _run_script(script_path):
        env = environ.copy()
        env["PYTHONPATH"] = "."

        cmd = ["python", script_path, "-h"]
        process = subprocess.run(cmd, capture_output=True, env=env)

        output = process.stdout.decode("utf-8").split("\n")
        errors = process.stderr.decode("utf-8")
        returncode = process.returncode

        assert errors == ""
        assert returncode == 0

        for line in output:
            print(line)

        return output
