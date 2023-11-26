'''
Parser for the `Tip` paragraph

Example
-------
>>> def func():
...     """
...     Tip
...     ---------
...     A tip
...
...     Tip: Another tip
...     """

'''
from miko.parsers.inline import InlineParser


class Tip(InlineParser):
    """
    The `Tip` paragraph parser
    """
    names = ["Tip", "Tips"]
