"""
Provides functions, classes, and constants used to interpret argparse actions
"""
import typing
import argparse
import pathlib

from functools import partial

from textual.widget import Widget
from textual import widgets

from .common import get_element_by_name

WidgetType = typing.Type[Widget]
WidgetBuilder = typing.Callable[[typing.Any], Widget]

# Store references to important argparse action types 
#   - this gets around warnings about private attribute access
HelpAction: typing.Type[argparse.Action] = getattr(argparse, "_HelpAction")
"""The ArgumentParser's action indicating that help text should be displayed"""
StoreAction: typing.Type[argparse.Action] = getattr(argparse, "_StoreAction")
"""The ArgumentParser's parameter class indicating that a value will be stored"""
SubParserAction: typing.Type[argparse.Action] = getattr(argparse, "_SubParsersAction")
"""
The ArgumentParser's parameter class indicating that this value decides finer 
grain details for what branching behavior requires
"""
StoreTrueAction: typing.Type[argparse.Action] = getattr(argparse, "_StoreTrueAction")
"""The ArgumentParser's parameter class whose presence indicates a `True` value"""
StoreFalseAction: typing.Type[argparse.Action] = getattr(argparse, "_StoreFalseAction")
"""The ArgumentParser's parameter class whose precence indicates a `False` value"""


def value_is_of_type(value_type: typing.Type, expected_type: typing.Type) -> bool:
    """
    Determines if the given type is of the expected type

    Answers "I got handed this type object - Can I consider the values of this are integers?"

    Args:
        value_type: The type to compare against
        expected_type: The type whose membership may direct behavior

    Returns:
        True if values of `value_type` may be treated as values of `expected_type`
    """
    if not isinstance(expected_type, typing.Type):
        return TypeError(
            "The type to compare against must by a type - received "
            f"'{expected_type}' (type={type(expected_type)})"
        )
    
    if not isinstance(value_type, typing.Type):
        return TypeError(
            f"The type to check must be a type - received {value_type} (type={type(value_type)})"
        )

    if value_type is expected_type:
        return True
    
    return issubclass(value_type, expected_type)


def get_widget_by_value_type(
    value_type: typing.Union[str, typing.Type]
) -> typing.Union[WidgetType, WidgetBuilder]:
    """
    Get the type of widget based on the type of value to represent

    Args:
        value_type: The type of value to represent

    Returns:
        The type of widget to use to represent the type of value and 
        specific values needed to represent it in the constructor
    """
    # If this is a str, we're assuming that we need to reach out and 
    # get this or a collection of widgets based on its name
    if isinstance(value_type, str):
        value_type = get_element_by_name(name=value_type)

    if not isinstance(value_type, typing.Type):
        raise TypeError(
            "Cannot determine what widget to use based off of "
            f"'{value_type}' (type={type(value_type)}). Only a type of "
            "value or the name of a type of value is allowed"
        )
    
    if value_is_of_type(value_type=value_type, expected_type=bool):
        return widgets.Switch
    
    # Make sure that 'type' is the correct parameter
    if value_is_of_type(value_type=value_type, expected_type=int):
        return partial(widgets.Input, type="integer")
    
    if value_is_of_type(value_type=value_type, expected_type=float):
        return partial(widgets.Input, type="number")

    if value_is_of_type(value_type=value_type, expected_type=pathlib.Path):
        # This needs to be something that indicates multiple widgets - a textbox and file selector
        raise NotImplementedError("Path input has not been implemented yet")

    return widgets.Input

def get_widget_by_action(action: argparse.Action) -> typing.Union[WidgetType, WidgetBuilder]:
    """
    Get the appropriate widget for an argparse action

    Args:
        action: The argparse action to interpret

    Returns:
        The type of widget to use or a function that will create it properly
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

    constructor = get_widget_by_value_type(action.type)

    return constructor
