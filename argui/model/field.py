"""
Defines the basic models used to demonstrate a field on the screen in a way that 
is easier for the library to understand than just the ArgumentParser
"""
import typing

from textual.widget import Widget
from textual.widgets import Input

import pydantic

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
    widget: typing.Union[str, typing.Type[Widget], CompoundWidget] = pydantic.Field(Input)

class SelectionField(Field):
    """Represents a field on the screen that acts a selector for more than one value"""
    exclusive: bool = pydantic.Field(True, description="Shows that only one of the values may be selected")
    options: typing.Union[
        typing.List[typing.Union[str, int]],
        typing.List[
            typing.Tuple[str, typing.Union[str, int]]
        ]
    ] = pydantic.Field(default_factory=list, description="The values available to select")
