from argparse import ArgumentParser
from collections import defaultdict
from sys import argv

from .command import Command
from .invokedcommand import InvokedCommand


class CCLI:
    """Chain Command Line Interface"""

    # Flag to indicate the next string is not a new command.
    # Used for situations where arguments and commands share the same name.
    SKIP_NEXT_COMMAND = "--cli-skip-command"
    # Default primary command key when none is provided
    NO_PRIMARY_COMMAND_KEY = "_ccli_none_key"

    # Primary command will parse commands first.
    def __init__(
        self,
        name="Chain CLI",
        primary_command_class=None,
        generate_help: bool = True,
        enable_chaining: bool = True,
        cli_args: list = None,
    ):
        """Creates a CCLI, loads command subclasses, and runs each invoked command.

        Args:
            name: Name of the command line interface.
            primary_command_class: Command to act as the default parser.
              The primary command will parse arguments until another command is invoked.
            generate_help: Automatically generate help text. Defaults to True.
            enable_chaining: Enables chaining of multiple commands together.  Defaults to True.
            cli_args:  Arguments to pass to the CCLI.  Defaults to argv, primarily used for testing.
        """
        if cli_args is None:
            cli_args = argv
        self.name = name
        self.generate_help = generate_help
        self.chaining = enable_chaining
        self.args = cli_args
        self.available_commands = {}
        self.invoked_commands = []

        if primary_command_class is not None:
            self.primary_command = InvokedCommand(primary_command_class.key)
            self.invoked_commands.append(self.primary_command)
        else:
            # Define the primary command but do not add it to the list of invoked commands.
            self.primary_command = InvokedCommand(CCLI.NO_PRIMARY_COMMAND_KEY)

        self._build_command_map()
        self._build_invoked_commands()
        self._instantiate_commands()
        self._run_commands()

    def _build_command_map(self):
        """Loops over all the subclasses of Command and adds their key (short key and alt key if
        available) and command class to the list of available commands.
        """
        for command in Command.__subclasses__():
            command_keys = [
                (command.key, True),
                (command.short_key, False),
                (command.alt_key, False),
            ]
            for key_type, required in command_keys:
                key_str = self._get_command_key(
                    key_type, command.__name__, required=required
                )
                if key_str is not None:
                    self.available_commands[key_str] = command

    def _get_command_key(self, key, command_name, required=False):
        """
        Returns the string value of a key for a command.  This handles strings and callables
        (such as properties) as keys.
        Raises an error if no string was created and the key is required.
        Returns None if the evaluated key is not a string.
        """
        c_key = key
        if callable(key):
            try:
                c_key = key()
            except TypeError:
                if required:
                    raise NotImplementedError(
                        "Incorrect key implementation for class: " + command_name
                    )
        if type(c_key) is not str and required:
            raise NotImplementedError("Key not found for class: " + command_name)
        return c_key

    def _build_invoked_commands(self):
        """
        Parses the arguments passed into the CCLI and assigns them to command classes.
        """
        skip_command = False
        current_command = self.primary_command

        for i, arg in enumerate(self.args[1:]):
            if arg == CCLI.SKIP_NEXT_COMMAND:
                skip_command = True
                continue

            if not skip_command and arg in self.available_commands:
                if self.chaining:
                    current_command = InvokedCommand(arg)
                    self.invoked_commands.append(current_command)
                    continue

                else:
                    # In single mode, add the rest of the arguments to the command.
                    # Use i + 2 because the list is starting at index one, from the slice in the for loop.
                    invoked_args = self.args[i + 2 :]
                    current_command = InvokedCommand(arg, args=invoked_args)
                    self.invoked_commands.append(current_command)
                    break

            skip_command = False
            current_command.args.append(arg)

    def _instantiate_commands(self):
        """
        Instantiates the invoked commands by creating class instances.
        If help (-h, --help) was passed into the primary command then handle help text before
        instantiation to prevent potential side effects of instantiating commands but not running them.
        """

        # If the command help is handled by the CCLI,
        # make the help text before parsing the remaining commands.
        # Python argparse will exit the program after displaying help text.
        if (
            self.generate_help
            and len(self.primary_command.args) > 0
            and self.primary_command.args[0] in ("-h", "--help")
        ):
            self._make_help_text(self.primary_command.args)

        for cmd in self.invoked_commands:
            parsed_args = self.available_commands[cmd.key].parse(cmd.args)
            cmd.instantiate(self.available_commands[cmd.key], parsed_args)

    def _run_commands(self):
        """
        Runs the invoked commands.
        """
        for cmd in self.invoked_commands:
            cmd.instance.run()

    def _make_help_text(self, args):
        """
        Utilizes argparse's help text generator to make help text for all the available commands.

        Args:
            args: List of arguments to parse help text for. Usually -h or --help but can be
              something else if the primary_command_class has a custom parser.
        """
        primary_command_cls = None
        if self.primary_command.key is not CCLI.NO_PRIMARY_COMMAND_KEY:
            primary_command_cls = self.available_commands[self.primary_command.key]

        if primary_command_cls is not None and primary_command_cls.parser is not None:
            parser = primary_command_cls.parser
            parser.prog = self.name
        else:
            parser = ArgumentParser(prog=self.name)

        sub = parser.add_subparsers(help="Available commands")

        available_commands_inverse = defaultdict(list)
        for key, command_class in self.available_commands.items():
            available_commands_inverse[command_class].append(key)

        for command_class, keys in available_commands_inverse.items():
            if self.primary_command.key in keys:
                continue

            all_keys = ",".join(keys)

            if (
                command_class.parser is not None
                and command_class.parser.description is not None
            ):
                help_text = command_class.parser.description
            else:
                help_text = "Run %s -h for more information" % all_keys

            sub.add_parser(all_keys, help=help_text)

        parser.parse_known_args(args)
