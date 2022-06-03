from argparse import ArgumentParser

from ccli import CCLI, Command


class RunCounter:
    run_count = 0

    @classmethod
    def run(cls):
        cls.run_count += 1


class Primary(RunCounter, Command):
    key = "primary"

    parser = ArgumentParser(prog="Primary Command", description="Primary command desc")
    parser.add_argument("-e", "--env", type=str, help="Primary CLI Environment")


class StartServer(RunCounter, Command):
    key = "start"
    short_key = "s"

    parser = ArgumentParser(prog="Server", description="Start the server.")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Start in debug mode."
    )
    parser.add_argument("-p", "--port", type=int, help="Server port")


class SeedDatabase(RunCounter, Command):
    key = "seed"
    alt_key = "seed-db"

    parser = ArgumentParser(
        prog="Database seed",
        description="Seed the database from a SQL file or list of files.",
    )
    parser.add_argument("sql_file", type=str, help="SQL seed file.", nargs="+")


class UnitTest(RunCounter, Command):
    key = "test"

    parser = ArgumentParser(prog="Unit Test", description="Run unit tests.")
    parser.add_argument("-d", "--debug", action="store_true", help="Debug tests.")
    parser.add_argument(
        "--cov", action="store_false", help="Run with code coverage, default true."
    )


class CleanDatabase(RunCounter, Command):
    key = "clean-db"


# Make this file runnable so help text can be tested.
if __name__ == "__main__":
    CCLI(name="Help Text Test", primary_command_class=Primary)
    print("output")
