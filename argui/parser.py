"""
Defines the overrides for the core ArgumentParser and the subparser classes
"""
import argparse

class ArgumentParser(argparse.ArgumentParser):
    """
    The overridden ArgumentParser class. This allows for the drop-in replacement behavior,
    makes sure that the `interactive` flag is present, and ensures that the calls to
    create subparsers creates subparsers that support the ArgUI framework
    """
    def __init__(
        self,
        prog = None,
        usage = None,
        description = None,
        epilog = None,
        parents = ...,
        formatter_class = argparse.ArgumentDefaultsHelpFormatter,
        prefix_chars = "-",
        fromfile_prefix_chars = None,
        argument_default = None,
        conflict_handler = "error",
        add_help = True,
        allow_abbrev = True,
        exit_on_error = True
    ):
        super().__init__(
            prog,
            usage,
            description,
            epilog,
            parents,
            formatter_class,
            prefix_chars,
            fromfile_prefix_chars,
            argument_default,
            conflict_handler,
            add_help,
            allow_abbrev,
            exit_on_error
        )
        self.add_argument(
            "-i",
            "--interactive",
            dest="interactive",
            action="store_true",
            help="Enter the script in interactive mode"
        )
