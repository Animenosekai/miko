"""
Defines what is empty
"""
import typing
import inspect


def is_empty(value: typing.Any):
    """Internal function to determine if the given value
    is considered as 'Empty' by the inspect module"""
    value_repr = str(value).strip().replace(" ", "")
    return ((value is inspect._empty)
            or (isinstance(value, inspect._empty))
            or (value_repr == "<class'inspect._empty'>")
            or (value is Empty)
            or (isinstance(value, Empty)))


class Empty:
    """Represents an empty element"""
