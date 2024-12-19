"""
Provides functions, classes, and constants used to interpret argparse actions
"""
import typing
import argparse

from textual.widget import Widget
from textual import widgets

# Store references to important argparse action types 
#   - this gets around warnings about private attribute access
HelpAction: typing.Type[argparse.Action] = getattr(argparse, "_HelpAction")
StoreAction: typing.Type[argparse.Action] = getattr(argparse, "_StoreAction")
SubParserAction: typing.Type[argparse.Action] = getattr(argparse, "_SubParserAction")
StoreTrueAction: typing.Type[argparse.Action] = getattr(argparse, "_StoreTrueAction")
StoreFalseAction: typing.Type[argparse.Action] = getattr(argparse, "_StoreFalseAction")

def get_widget_by_value_type(value_type: typing.Union[str, typing.Type]) -> typing.Tuple[typing.Type[Widget], typing.Dict[str, typing.Any]]:
    """
    Get the type of widget based on the type of value to represent

    Args:
        value_type: The type of value to represent

    Returns:
        The type of widget to use to represent the type of value and specific values needed to represent it in the constructor
    """
    # TODO: Actually implement this
    if value_type:
        pass

def get_widget_by_action(action: argparse.Action) -> typing.Type[Widget]:
    """
    Get the appropriate widget for an argparse action

    Args:
        action: The argparse action to interpret

    Returns:
        A widget the appropriately matches the given parameter
    """
    if isinstance(action, HelpAction):
        raise TypeError("The help command is not an appropriate screen element")

    if not isinstance(action, StoreAction):
        raise TypeError(
            "Only actions that may store a value may be represented on the screen. "
            f"Received {action} (type={type(action)})"
        )

    if isinstance(action, (StoreTrueAction, StoreFalseAction)):
        return widgets.Switch

    if action.choices:
        if isinstance(action.nargs, int) and action.nargs > 1 or action.nargs in ("+", "*"):
            return widgets.SelectionList
        return widgets.Select

    return widgets.Input
