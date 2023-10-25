'''
Parser for the `Changelog` paragraph

Example
-------
>>> def func():
...     """
...     Changelog
...     ---------
...     element1: options1, options2
...         element1 description
...     element2: options1, options2
...         element2 description
...     """
'''
from miko.parsers.map import MapParser


class Changelog(MapParser):
    """Parser for the `Changelog` paragraph"""
    names = ["Changelog", "Changes"]
