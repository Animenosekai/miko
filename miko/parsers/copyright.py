'''
Parser for the `Copyright` paragraph

Example
-------
>>> def func():
...     """
...     Copyright
...     ---------
...     element1: options1, options2
...         element1 description
...     element2: options1, options2
...         element2 description
...     """
'''
from miko.parsers.map import MapParser


class Copyright(MapParser):
    """Parser for the `Copyright` paragraph"""
    names = ["Copyright", "Copyrights", "Authors", "Author"]
