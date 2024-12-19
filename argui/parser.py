"""
Defines the overrides for the core ArgumentParser and the subparser classes
"""
import typing
import argparse

import argui.model

Fields = typing.List[argui.model.Field]
WorkflowMapping = typing.Dict[str, Fields]
Workflows = typing.Dict[str, typing.Union[Fields, WorkflowMapping]]

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

    def to_model(self) -> Workflows:
        """
        Interpret the parser as a series of fields for the terminal

        Returns:
            Fields that should appear on the screen, organized by workflow name
        """
        workflows: Workflows = {}

        return workflows