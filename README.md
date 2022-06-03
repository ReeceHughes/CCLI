# Chain Command Line Interface

## Description:

Easily make classes runnable from the command line and chain multiple commands together.

## Installation

    pip install "git+ssh://git@github.com/ReeceHughes/CCLI.git#egg=ccli"

## Usage

Implement the `Command` interface to make a class runnable from the command line.

- `key` (Required): The `key` is how the command is invoked from the command line.
- `run` (Optional): Called when the command is invoked from the command line.
- `short_key` (Optional): Same as `key` but typically only one letter.
- `alt_key` (Optional): Same as `key` but with an alternate name.

Example:

    from ccli import Command

    class StartServer(Command):
	    key = "start"
	    short_key = "s"

	    def run(self):
	        print('Starting the server')


If `__init__` is implemented in a command, make sure it accepts a list of command line arguments as a positional argument.

    class StartServer(Command):
	    def __init__(self, cli_args):
	        self.args = cli_args


To create the CCLI, just create a CCLI class.

    from ccli import CCLI

    CCLI()


See [backend_project_commands.py](tests/backend_project_commands.py) for a complete example.

