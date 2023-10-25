'''
Parser for the `Raises` paragraph

Example
-------
>>> def func():
...     """
...     Raises
...     ---------
...     element1: options1, options2
...         element1 description
...     element2: options1, options2
...         element2 description
...     """
'''
from miko.parsers.map import MapParser


class Raises(MapParser):
    """Parser for the `Raises` paragraph"""
    names = ["Raises", "Raise", "Raising",
             "Exceptions", "Exception", "Errors", "Error"]
