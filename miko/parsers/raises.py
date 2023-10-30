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

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if self.raised:
            for exc in self.raised:
                if hasattr(exc, "__name__"):
                    name = exc.__name__
                else:
                    name = str(exc if exc else "")
                if name and not name in self:
                    self[name] = self.element(name=name,
                                              **self.extra_arguments)

    @property
    def raised(self):
        """The raised exceptions"""
        return self.extra_arguments.get("raised", [])
