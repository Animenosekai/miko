'''
Parser for the `Yields` paragraph

Example
-------
>>> def func():
...     """
...     Yields
...     ----------
...     element1: options1, options2
...         element1 description
...     element2: options1, options2
...         element2 description
...     """
'''
from miko.parsers.map import MapParser


class Yields(MapParser):
    """Parser for the `Yields` paragraph"""
    names = ["Yields", "Yield", "Yielding"]
