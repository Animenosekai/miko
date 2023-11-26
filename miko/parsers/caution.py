'''
Parser for the `Caution` paragraph

Example
-------
>>> def func():
...     """
...     Caution
...     ---------
...     A caution message
...
...     Caution: Another caution message
...     """
'''
from miko.parsers.inline import InlineParser


class Caution(InlineParser):
    """The `Caution` paragraph parser"""

    names = ["Caution"]

