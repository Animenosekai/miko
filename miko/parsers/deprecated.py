'''
Parser for the `deprecated` flag

Example
-------
>>> def func():
...     """
...     ! DEPRECATED !
...
...     (description)
...     """

'''
from miko.parsers.flag import FlagParser


class Deprecated(FlagParser):
    """
    The `deprecated` flag parser
    """
    names = ["DEPRECATED", "DEPRECATION"]
