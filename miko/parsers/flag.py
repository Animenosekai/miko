"""Defines the flag parsers base class"""
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
