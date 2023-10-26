'''
Defines the flag parsers base class

A flag is what describes a boolean value in a docstring

If the flag is present, it will be set to True, otherwise it will be set to False

Example
-------
>>> def func():
...     """
...     This is a function
...
...     ! FLAG
...     ! YOU'RE COOL
...     
...     (description)
...     """
'''
import typing

from miko.parsers.parser import Parser


class FlagParser(Parser):
    """A flag parser"""
    element: typing.Type[bool] = bool
    elements: typing.List[bool]

    def set_flag(self):
        """Sets the flag"""
        self.elements.append(True)

    def dumps(self, indent: int = 4, prefix: str = "!"):
        if self.elements:
            return f"{prefix} {self.name}"
        return ""

    @property
    def flag(self):
        return len(self.elements) > 0

    @property
    def exported(self):
        """The exported data"""
        return self.flag

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.flag})"
