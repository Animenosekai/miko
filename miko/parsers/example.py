'''
Parser for the `Example` paragraph

Example
-------
>>> def func():
...     """
...     Example
...     -------
...     A paragraph describing an example
...     """

'''
from miko.parsers.inline import InlineParser


class Example(InlineParser):
    """
    The `Example` paragraph parser
    """
    names = ["Example", "Examples"]
