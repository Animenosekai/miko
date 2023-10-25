"""Defines the base class for inline parsers"""
import typing

from miko.parsers.parser import Parser


class InlineParser(Parser):
    """An inline section parser"""
    element: typing.Type[str] = str
    elements: typing.List[str]

    def append(self, content: str):
        """Extends the current """
        self.elements.append(content)

    def dumps(self, indent: int = 4):
        one_liners = []
        multi_liners = []
        for element in self.elements:
            if "\n" in element:
                multi_liners.append(element)
            else:
                one_liners.append(element)

        result = ""

        for element in one_liners:
            result += f"{self.name}: {element}\n\n"

        for element in multi_liners:
            result += f"{self.name}\n"
            result += f"{'-' * len(self.name)}\n"
            result += element
            result += "\n\n"

        return result.strip().strip("\n")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({len(self.elements)} elements)"
