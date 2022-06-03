class InvokedCommand:
    """Contains information about a command once it has been invoked in the CLI."""

    def __init__(self, key, args=None, instance=None):
        if args is None:
            args = []

        self.key = key
        self.args = args
        self.instance = instance
        self.output = None

    def instantiate(self, cmd_class, args):
        self.args = args
        self.instance = cmd_class(self.args)

    def __repr__(self):
        return "InvokedCommand(key=%s, type=%s, args=%s)" % (
            self.key,
            type(self.instance).__name__,
            self.args,
        )
