"""
Defines the basic models used to demonstrate a field on the screen in a way that 
is easier for the library to understand than just the ArgumentParser
"""
import typing
import re
import string
import pathlib

from textual import widgets
from textual.widget import Widget
from textual.containers import Container

import pydantic

from argui.utilities import actions

INVALID_CHARACTER_PATTERN: re.Pattern = re.compile(f"[{string.whitespace + string.punctuation}]+")


class CompoundWidget(pydantic.BaseModel):
    """Represents a widget that my be constructed by combining other widgets"""

class Field(pydantic.BaseModel):
    """Represents a field on the screen"""
    index: int = pydantic.Field(description="The index of the field on the screen", ge=0)
    name: str = pydantic.Field(description="The name of the field")
    help: typing.Optional[str] = pydantic.Field(None, description="Help text for the field")
    default: typing.Any = pydantic.Field(None, description="The default value for the field")
    flags: typing.List[str] = pydantic.Field(
        default_factory=list,
        description="CLI Flags for the field"
    )
    type: typing.Union[typing.Type, typing.Callable[[str], typing.Any], str] = pydantic.Field(
        str,
        description="The type that this value should be within the python application"
    )
    required: bool = pydantic.Field(False)
    widget: typing.Union[str, typing.Type[Widget], CompoundWidget] = pydantic.Field(
        "textual.widgets.Input",
        description="What core widget to use to render the field"
    )
    widget_parameters: typing.Dict[str, typing.Any] = pydantic.Field(
        default_factory={},
        description="Specialized parameters needed to express how to build the final widget"
    )

    @property
    def safe_name(self) -> str:
        """
        A name that may be used for the field that does not contain illegal characters for id purposes
        """


    def build_widget(self) -> Container:
        """
        Build the element that represents the field on the screen

        Returns:
            A widget instance to place on the screen
        """
        sanitized_name: str = sanitize_name(self.name)
        widget_id: str = f"{self.index}_{sanitized_name}"
        container_elements: typing.List[Widget] = [
            widgets.Label(self.name, id=f"{widget_id}_label")
        ]
        
        if self.type == pathlib.Path:
            pass
        else:
            input_class = actions.get_

        container = Container(
            *container_elements,
            name=sanitized_name,
            id=f"{self.index}_{sanitized_name}"
        )
        return container

class SelectionField(Field):
    """Represents a field on the screen that acts a selector for more than one value"""
    exclusive: bool = pydantic.Field(True, description="Shows that only one of the values may be selected")
    options: typing.Union[
        typing.List[typing.Union[str, int]],
        typing.List[
            typing.Tuple[str, typing.Union[str, int]]
        ]
    ] = pydantic.Field(default_factory=list, description="The values available to select")

def sanitize_name(name: str, replacement: str = "_") -> str:
    """
    Replace all invalid characters within a name

    Args:
        name: The name to sanitize
        replacement: The characters to use to replace invalid characters

    Returns:
        The name that is safe to use as an id
    """
    invalid_characters: str = (string.punctuation + string.whitespace).replace("_", "")
    if replacement != "_" and replacement in invalid_characters:
        raise ValueError(
            f"Cannot use '{replacement}' as a replacement character - it is not a sanitary character. "
            f"Please choose a character that is not one of the following: {invalid_characters}"
        )

    if not name:
        raise ValueError("Cannot sanitize an empty name")

    # Repeatedly replace invalid characters
    #   A string like:
    #       ? this+ -?\ /. is # a    ____ string
    #   will become:
    #       __this________is___a________string
    #   keep running it until it becomes an acceptable:
    #       _this_is_a_string
    clean_name: str = name
    while re.search(f"[{invalid_characters}]+", clean_name):
        clean_name = INVALID_CHARACTER_PATTERN.sub(
            replacement,
            name
        )

    # A leading digit isn't valid in some situations - prepend it with the replacement to 
    if clean_name[0] in string.digits:
        clean_name = replacement + clean_name

    return clean_name