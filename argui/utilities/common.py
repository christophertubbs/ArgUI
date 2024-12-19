"""
Contains common functions and constants that don't necessary have an obvious home
"""
import typing
import types

_SENTINEL = object()

def get_element_by_name(name: str, context: typing.Union[typing.Dict[str, typing.Any], types.ModuleType] = None) -> typing.Any:
    """
    Try to find an object by its name within the current code context

    Args:
        name: The name of the element to find. Names with '.' will be used to help traverse a nested context
        context: Where to look. Defaults to globals

    Returns:
        The object if it could be found
    """
    if not name:
        raise ValueError("Cannot find an element if its name was not supplied")
    
    if context is None:
        context = globals()

    head_key: str = name.split(".")[0] if '.' in name else name
    tail_key: typing.Optional[str] = ".".join(name.split(".")[1:]) if '.' in name else None
    current_context: typing.Union[typing.Dict[str, typing.Any], types.ModuleType] = context

    def key_in_context(key: str, context_to_search: typing.Union[typing.Mapping, types.ModuleType]) -> bool:
        """
        Check to see if the current key is in the given context

        Args:
            key: The key to look for
            context_to_search: The object that might contain a value mapped to the key

        Returns:
            True if the key is in the context
        """
        if key is None:
            return False
        
        if not isinstance(current_context, (typing.Mapping, types.ModuleType)):
            raise TypeError(
                "Cannot search for an element in the given context - only maps and modules "
                f"may be traversed and encountered a {type(current_context)}"
            )
        
        if isinstance(context_to_search, typing.Mapping):
            return key in context_to_search
        
        if isinstance(context_to_search, types.ModuleType):
            return hasattr(context_to_search, key)

        return False

    found_value: typing.Any = _SENTINEL

    while key_in_context(head_key, current_context):
        if not isinstance(current_context, (typing.Mapping, types.ModuleType)):
            raise TypeError(
                "Cannot search for an element in the given context - only maps and modules "
                f"may be traversed and encountered a {type(current_context)}"
            )

        if hasattr(current_context, head_key):
            found_value = getattr(current_context, head_key, _SENTINEL)
        # If current_context is a mapping, try looking up head_key
        elif isinstance(current_context, typing.Mapping):
            found_value = current_context.get(head_key, _SENTINEL)

        if found_value is _SENTINEL and key_in_context("__builtins__", current_context):
            builtin_values = get_element_by_name("__builtins__", current_context)
            if key_in_context(head_key, builtin_values):
                if isinstance(builtin_values, typing.Mapping):
                    found_value = builtin_values.get(head_key, _SENTINEL)
                else:
                    found_value = getattr(builtin_values, head_key, _SENTINEL)

        if found_value is _SENTINEL:
            raise KeyError(f"There are no elements found via '{name}' in the given context")

        if tail_key:
            if '.' in tail_key:
                head_key, tail_key = tail_key.split(".", maxsplit=1)
            else:
                head_key = tail_key
                tail_key = None
        else:
            head_key = None

        current_context: typing.Union[typing.Dict[str, typing.Any], types.ModuleType] = found_value

    if found_value == _SENTINEL:
        raise KeyError(f"There are no objects within the given context with a key of '{name}'")

    return found_value
