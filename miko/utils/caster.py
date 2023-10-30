"""
Casts element to the right type
"""
import builtins
import json
import pathlib
import subprocess
import types
import typing

from miko.utils.empty import is_empty


def try_retrieve_type(value: typing.Union[str, type]) -> typing.List[typing.Union[str, type, None]]:
    """Tries to retrieve the types from a string"""
    if not isinstance(value, str):
        if is_empty(value):
            return []
        if typing.get_origin(value) in (typing.Union, types.UnionType):
            results = []
            for result in typing.get_args(value):
                results.extend(try_retrieve_type(result))
            return results
        return [typing.get_origin(value) or value]

    processing = str(value).strip().lower()  # List => list
    processing = processing.removeprefix("typing.")  # typing.list => list

    # If we have a Union type
    if "|" in processing:
        results = []
        for value in processing.split("|"):
            results.extend(try_retrieve_type(value))
        return results

    if processing.count("[") == processing.count("]"):  # list[dict[str, int]] => list
        # If we have a typing.Union type
        if processing.startswith("union") or processing.startswith("optional"):
            inside, _, _ = processing.partition("[")[2].rpartition("]")
            results = []
            for val in inside.split(","):
                results.extend(val)
            if processing.startswith("optional"):
                results.append(None)
            return results

        # If we have a generic type, we don't really care about what's inside
        processing, _, _ = processing.partition("[")

    # We assume that there is only 1 type to return from now on

    # Handling None types
    if processing == "none":
        return [None]

    if processing == "path" or processing == "pathlib.path":
        return [pathlib.Path]

    if processing == "popen" or processing == "subprocess.popen":
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
