'''
Parser for the `Important` paragraph

Example
-------
>>> def func():
...     """
...     Important
...     ---------
...     A important note
...
...     Important: Another important note
...     """

'''
from miko.parsers.inline import InlineParser


class Important(InlineParser):
    """
    The `Important` paragraph parser
    """
    names = ["Important", "Important Notice"]
