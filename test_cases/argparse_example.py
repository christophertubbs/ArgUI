#!/usr/bin/env python3
"""
A complex example of how to use the argument parser
"""
import asyncio
import logging
import sys
import typing
import os
import pathlib

from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter

_APPLICATION_NAME = "ArgParse Example"
"""The name of the application within this script"""

SUCCESS_CODE: typing.Final[int] = 0
"""A return code indicating that this script ran until a successful completion"""

ERROR_CODE: typing.Final[int] = 1
"""A return code indicating that this script exitted due to an error"""


class CLIInputs:
    """Parameters parsed from the command line"""
    def __init__(self, *args, **kwargs) -> None:
        self.__interactive = kwargs.get("interactive", False)
        self.args = None
        self.__parse(args)

    @property
    def interactive(self):
        return self.__interactive

    def __parse(self, args):
        """Parse arguments from the command line"""
        parser = ArgumentParser(
            prog=_APPLICATION_NAME,
            description=__doc__,
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            "-i",
            "--interactive",
            dest="interactive",
            action="store_true",
            default=False,
            help="Launch the application in an interactive mode"
        )
        subparsers = parser.add_subparsers(dest="command", required=True)

        parser_create = subparsers.add_parser(
            "create",
            help="Create a file or directory"
        )
        parser_create.add_argument(
            "type",
            choices=["file", "dir"],
            help="Type of item to create"
        )
        parser_create.add_argument(
            "name",
            help="Name of file or directory to create"
        )
        parser_create.add_argument(
            "--content",
            help="Content to write to a file (only valid for files)"
        )
        parser_create.set_defaults(func=create_file_or_dir)

        parser_delete = subparsers.add_parser(
            "delete",
            help="Delete a file or directory"
        )
        parser_delete.add_argument(
            "name",
            help="Name of file or directory to delete"
        )
        parser_delete.set_defaults(func=delete_file_or_dir)

        parser_list = subparsers.add_parser(
            "list",
            help="List all files or directories"
        )
        parser_list.add_argument(
            "--type",
            choices=["file", "dir"],
            help="Filter by type (file or directory)"
        )
        parser_list.add_argument(
            "--path",
            help="Path to list files or directories from",
            default="."
        )
        parser_list.set_defaults(func=list_files)

        parser_copy = subparsers.add_parser(
            "copy",
            help="Copy a file or directory to a new location"
        )
        parser_copy.add_argument(
            "source",
            type=pathlib.Path,
            help="source file or directory"
        )
        parser_copy.add_argument(
            "destination",
            type=pathlib.Path,
            help="destination file or directory for the copy"
        )
        parser_copy.set_defaults(func=copy_file)

        self.args = parser.parse_args(args or None)
        self.__interactive = self.args.interactive

def create_file_or_dir(args):
    if args.type == "file":
        print(f"File '{args.name}' created successfully")
    elif args.type == "dir":
        os.makedirs(args.name, exist_ok=True)
        print(f"Directory '{args.name}' created successfully")

def delete_file_or_dir(args):
    if os.path.exists(args.name):
        if os.path.isfile(args.name):
            print(f"File '{args.name}' deleted successfully")
        elif os.path.isdir(args.name):
            print(f"Directory '{args.name}' deleted successfully")
    else:
        print(f"File '{args.name}' does not exist")

def list_files(args):
    path = args.path or '.'
    if os.path.exists(path) and os.path.isdir(path):
        items = os.listdir(path)
        if args.type == 'file':
            items = [
                item
                for item in items
                if os.path.isfile(os.path.join(path, item))
            ]
        elif args.type == 'dir':
            items = [
                item
                for item in items
                if os.path.isdir(os.path.join(path, item))
            ]
        print(os.linesep.join(items) if items else f"No {args.type or 'items'} found in {path}")
    else:
        print(f"Path '{path}' does not exist")

def copy_file(args):
    if os.path.isfile(args.source):
        print(f"File '{args.source}' copied to '{args.destination}'")
    else:
        print(f"File '{args.source}' does not exist or is not a file")

async def run(inputs: CLIInputs) -> int:
    """
    The application logic
    
    Args:
        inputs: parameters that would normally be passed to a CLI 

    Returns:
        An exit code describing the status of the application on exit
    """
    # Write application logic here
    return SUCCESS_CODE


async def main(*args) -> int:
    """
    Parses the CLI and runs the application
    
    Returns:
        The status code that dictates how this application should exit
    """
    try:
        parameters = CLIInputs(*args)
    except Exception as e:
        logging.error(f"Failed to parse CLI inputs: {sys.argv}", exc_info=e)
        return ERROR_CODE

    try:
        if parameters.interactive:
            # Run the interactive code
            return 0
        return await run(parameters)
    except Exception as e:
        logging.error(f"{_APPLICATION_NAME} Failed", exc_info=e)
        return ERROR_CODE


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
