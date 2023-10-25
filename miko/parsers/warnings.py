'''
Parser for the `Warning` paragraph

Example
-------
>>> def func():
...     """
...     Warning
...     ---------
...     A warning
...
...     Warning: Another warning about using the element
...     """

'''
from miko.parsers.inline import InlineParser


class Warnings(InlineParser):
    """
    The `Warning` paragraph parser
    """
    names = ["Warning", "Warnings"]
