'''
Parser for the `Notes` paragraph

Example
-------
>>> def func():
...     """
...     Notes
...     -------
...     A note
...
...     Note: Another note
...     """

'''
from miko.parsers.inline import InlineParser


class Notes(InlineParser):
    """
    The `Notes` paragraph parser
    """
    names = ["Note", "Notes", "See also"]
