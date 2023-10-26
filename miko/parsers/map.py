'''
This defines the listed element parsers

"Mapped elements" refers to docstring paragraphs where multiple items can be mapped

Example
-------
>>> def func():
...     """
...     Paragraph
...     ---------
...     element1: options1, options2
...         element1 description
...     element2: options1, options2
...         element2 description
...     """
'''
import typing

from miko.parsers.parser import Parser, Element


class MapElement(Element):
    """An item in the map"""
    name: str
    """The name for the map item"""

    options: typing.Set[str]
    """
    The options for the element

    Example
    -------
    element1: option1, option2
              ^^^^^^^  ^^^^^^^
        (content)
    """

    def __init__(self, name: str,
                 options: typing.Optional[typing.Iterable[str]] = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = str(name)
        options = (self._normalize_option(opt) for opt in (options or []))
        self.options = set(opt for opt in options if opt)

    def _normalize_option(self, option: str):
        return str(option).strip().lower()

    def extend_options(self, options: typing.Iterable[str]):
        """
        Extends the options with the provided values

        Parameters
        ----------
        options: Iterable[str]
            Options to add to the options
        """
        options = (self._normalize_option(opt) for opt in options)
        self.options.update(opt for opt in options if opt)

    def render_options(self) -> str:
        """Renders the options"""
        return ", ".join(self.options)

    def dumps(self, indent: int = 4) -> str:
        """
        Renders the element

        Parameters
        ----------
        indent: int, default = 4
            The indentation level
        """
        result = self.name
        options = self.render_options()
        if options:
            result += f": {options}"
        result += "\n"
        for line in self.body.splitlines():
            result += " " * indent
            result += line
            result += "\n"
        return result

    @property
    def exported(self):
        return {
            **super().exported,
            "name": self.name,
            "options": list(self.options)
        }


class MapParser(Parser):
    """A parser for map paragraphs"""
    element: typing.Type[MapElement] = MapElement
    elements: typing.List[MapElement]

    def extend(self, content: str) -> None:
        """
        Parses and adds new content to the paragraph

        Parameters
        ----------
        content: str
            The content to add to the paragraph
        """
        current = None
        for line in str(content).splitlines():
            # If the line is indented
            if line.startswith(" ") and current:
                self[current].append_body(line)
                continue
            # If the line is not indented, we are outside of an element scope
            # element1: option1, option2
            current, _, options = line.partition(":")
            current = current.strip()
            opt = options.strip().split(",")
            try:
                self[current].extend_options(opt)
            except KeyError:
                # Not declared yet
                # We need to create a new element
                self.elements.append(self.element(name=current, options=opt,
                                                  **self.extra_arguments))

    def dumps(self, indent: int = 4) -> str:
        result = ""
        if self.elements:
            result = f"{self.name}\n"
            # a minimum of 3 hyphens
            result += f"{'-' * max(len(self.name), 3)}\n"

            for element in self.elements:
                result += element.dumps(indent=indent)

        return result.strip().strip("\n")

    def __getitem__(self, key: str):
        key = str(key)
        for element in self.elements:
            if element.name == key:
                return element
        raise KeyError(
            f"The given name '{key}' does not seem to be an element")

    def __setitem__(self, key: str, value: MapElement):
        key = str(key)
        value.name = key
        for index, element in enumerate(self.elements):
            if element.name == key:
                self.elements[index] = value
                return
        self.elements.append(value)

    def __delitem__(self, key: str):
        for index, element in enumerate(self.elements):
            if element.name == key:
                self.elements.pop(index)
                return

    def __iter__(self):
        return iter(self.elements)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({[e.name for e in self.elements]})"
