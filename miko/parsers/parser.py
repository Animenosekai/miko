"""
Defines the base parser
"""
import typing


class Element:
    """Represents an element in a docstring paragraph"""
    body: str
    """
    The body of the element

    Example
    -------
    element1: option1, option2
        This is a long body
        ^^^^^^^^^^^^^^^^^^^
    """

    extra_arguments: typing.Dict[str, typing.Any]
    """The extra arguments passed in with the parser"""

    def __init__(self, **kwargs) -> None:
        self.body: str = ""
        self.extra_arguments = kwargs

    def append_body(self, value: str):
        """
        Appends the given value to the body of the element

        Parameters
        ----------
        value: str
            The string to append to the body
        """
        value = str(value).strip()
        if not self.body:
            self.body = value.strip("\n")
        else:
            self.body += "\n" + value.strip("\n")


class Parser:
    """The base class for a parser"""
    names: typing.List[str]
    """The names of the section (will be normalized)"""
    element: typing.Type
    """The element type"""
    elements: typing.List[typing.Type]
    """Elements parsed in the docstring paragraph"""
    extra_arguments: typing.Dict[str, typing.Any]
    """The extra arguments passed in with the parser"""

    def __init__(self, **kwargs) -> None:
        self.elements = []
        self.extra_arguments = kwargs

    @property
    def name(self):
        """The default name of the section"""
        if self.names:
            return self.names[0]
        return self.__class__.__name__

    def dumps(self, indent: int = 4) -> str:
        """Renders the docstring back"""
        raise NotImplementedError(
            "Tried to render the docstring back with a parser that wasn't fully implemented")

    def __getattr__(self, attr: str):
        try:
            return getattr(self.elements, attr)
        except AttributeError:
            # If not an attribute, might be an element
            return self[attr]

    def __getitem__(self, key):
        return self.elements[key]

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def __contains__(self, element: str):
        try:
            _ = self[element]
            return True
        except KeyError:
            return False
