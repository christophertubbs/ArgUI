"""
Defines models that describe a specific operation
"""
from __future__ import annotations
import typing
import argparse

import pydantic

from .field import Field

# Store references to important argparse action types 
#   - this gets around warnings about private attribute access
HelpAction: typing.Type[argparse.Action] = getattr(argparse, "_HelpAction")
StoreAction: typing.Type[argparse.Action] = getattr(argparse, "_StoreAction")
SubParserAction: typing.Type[argparse.Action] = getattr(argparse, "_SubParserAction")
StoreTrueAction: typing.Type[argparse.Action] = getattr(argparse, "_StoreTrueAction")
StoreFalseAction: typing.Type[argparse.Action] = getattr(argparse, "_StoreFalseAction")

def is_interactive_flag(action: argparse.Action) -> bool:
    """
    Determines if the given CLI action/parameter is used to indicate that the app should run 
    in interactive mode

    Args:
        action: The CLI action/parameter to investigate

    Returns:
        True if the action/parameter is used for indicating that the app should run in interactive mode
    """
    if not isinstance(action, StoreTrueAction):
        return False
    
    return not action.required and action.dest.lower() == "interactive"

class Workflow(pydantic.BaseModel):
    """
    Represents the fields and screen elements that will appear in the terminal

    Typically shares a 1:1 relationship with an `argparse.ArgumentParser`
    """
    name: typing.Optional[str] = pydantic.Field(
        None,
        description="The name of the workflow. Typically a 1:1 match with an `argparse.ArgumentParser::prog`"
    )
    description: typing.Optional[str] = pydantic.Field(
        None,
        description="Information that describes what the workflow does"
    )
    epilog: typing.Optional[str] = pydantic.Field(
        None,
        description="Additional footnotes about the workflow"
    )
    fields: typing.List[Field] = pydantic.Field(
        default_factory=list,
        description="The fields that should appear on the workflow screen",
        min_length=1
    )
    subworkflows: typing.Dict[str, Workflow] = pydantic.Field(
        default_factory=dict,
        description="Workflows that may be embedded within the workflow mapped to their name/command"
    )
    action: typing.Optional[str] = pydantic.Field(
        None,
        description="What the workflow should do when submitted"
    )

    @classmethod
    def from_parser(cls, parser: argparse.ArgumentParser) -> Workflow:
        """
        Creates a workflow from a built ArgumentParser

        Returns:
            A workflow covering what the parser intends to do
        """
        name: str = parser.prog
        epilog: typing.Optional[str] = parser.epilog
        description: typing.Optional[str] = parser.description
        fields: typing.List[Field] = []
        subworkflows: typing.Dict[Workflow] = {}

        for action in getattr(parser, "_actions", []):
            if is_interactive_flag(action) or isinstance(action, HelpAction):
                continue

            if isinstance(action, StoreAction):
                # Determine what sort of value is stored here - is it one or more values?
                pass
            elif isinstance(action, SubParserAction):
                for command_name, command in action.choices.items():
                    subworkflow = cls.from_parser(parser=command)
                    subworkflows[command_name] = subworkflow

        new_workflow = cls(
            name=name,
            epilog=epilog,
            description=description,
            fields=fields,
            subworkflows=subworkflows
        )

        return new_workflow



    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.name or 'Untitled'}{': ' + self.description if self.description else ''}"
