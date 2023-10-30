"""
Casts element to the right type
"""
import ast
import builtins
import dataclasses
import json
import pathlib
import subprocess
import types
import typing

from miko import static
from miko.utils.empty import is_empty


@dataclasses.dataclass(frozen=True)
class Callable:
    """Represents a callable type"""
    arg_types: typing.Tuple[typing.Tuple["Type"]]
    """The types for the arguments"""
    return_type: typing.Tuple["Type"]
    """The type for the return value"""

    def __str__(self) -> str:
        parameters = []

        def stringify(t):
            if hasattr(t, "__name__"):
                return t.__name__
            return str(t)

        for param in self.arg_types:
            parameters.append(" | ".join([stringify(p) for p in param]))

        return f"({', '.join(parameters)}) -> {' | '.join([stringify(p) for p in self.return_type])}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({str(self)})"


Type = typing.Union[str, type, None, Callable]


def try_retrieve_type(value: typing.Union[str, type], filename: typing.Optional[str] = None) -> typing.List[Type]:
    """Tries to retrieve the types from a string"""
    filename = filename or "<unknown>"
    if not isinstance(value, str):
        if is_empty(value):
            return []

        if typing.get_origin(value) is typing.Callable:
            results: typing.List[Type] = []
            results.append(Callable(
                arg_types=tuple([tuple(try_retrieve_type(val, filename=filename))
                           for val in typing.get_args(value)[0]]),
                return_type=tuple(try_retrieve_type(typing.get_args(value)[1],
                                                    filename=filename))
            ))
            return results

        if typing.get_origin(value) in (typing.Union, types.UnionType):
            results = []
            for result in typing.get_args(value):
                results.extend(try_retrieve_type(result, filename=filename))
            return results
        return [typing.get_origin(value) or value]

    # processing = str(value).strip().lower()  # List => list
    processing = str(value).strip()  # list    => list
    processing = processing.removeprefix("typing.")  # typing.list => list

    # If we have a Union type
    if "|" in processing:
        results = []
        for value in processing.split("|"):
            results.extend(try_retrieve_type(value, filename=filename))
        return results

    processing_lower = processing.lower()
    if processing.count("[") == processing.count("]"):  # list[dict[str, int]] => list
        # If we have a typing.Union type
        if processing_lower.startswith("union") or processing_lower.startswith("optional"):
            inside, _, _ = processing.partition("[")[2].rpartition("]")
            results = []
            for val in inside.split(","):
                results.extend(val)
            if processing_lower.startswith("optional"):
                results.append(None)
            return results

        # If we have a generic type, we don't really care about what's inside
        processing, _, _ = processing.partition("[")
        processing_lower = processing.lower()
    else:
        if filename:
            raise SyntaxError(f"The number of brackets don't match in: `{value}` "
                              f"(file: {filename})")
        raise SyntaxError(f"The number of brackets don't match in: `{value}`")

    # We assume that there is only 1 type to return from now on

    if "->" in processing:
        parsed = ast.parse(processing, mode="func_type", filename=filename)
        results = []
        results.append(Callable(
            arg_types=tuple([tuple(try_retrieve_type(static.get_dot_path(arg), filename=filename))
                       for arg in parsed.argtypes]),
            return_type=tuple(try_retrieve_type(static.get_dot_path(parsed.returns),
                                                filename=filename))
        ))
        return results

    # Handling None types
    if processing_lower == "none":
        return [None]

    if processing_lower == "path" or processing_lower == "pathlib.path":
        return [pathlib.Path]

    if processing_lower == "popen" or processing_lower == "subprocess.popen":
        return [subprocess.Popen]

    try:
        # If the given element is global (list, str, int, ...) return it
        return [getattr(builtins, processing)]
    except AttributeError:
        pass

    # We failed to do anything with the type, return it as a string
    # This might happen for example when you provide dot path elements (translatepy.Language)
    return [str(value)]


def try_cast(value: str,
             types: typing.Set[typing.Union[str, None, type]]) -> typing.Union[str, typing.Any]:
    """
    Tries casting the given value

    Parameters
    ----------
    value: str
        The value to cast
    types: set[str, (str) -> Any]
        The types to try casting to
    """
    value = str(value).strip()

    # If the provided value is pretty simple,
    # JSON should be able to decode it (A simple list or dictionary for example)
    try:
        return json.loads(value)
    except Exception:
        pass

    if value == "None":
        return None

    # If the value is not simple (A complex number for example)
    for cast in types:
        try:
            if cast and not isinstance(cast, str):
                return cast(value)
        except Exception:
            continue

    # If failed to do anything, return it as a string at least
    return str(value)
