"""
miko.py

Contains the main code for the Miko documentation style
"""

import inspect
import sys
import types
import typing

import miko.parser.example as example_parsers
import miko.parser.list as list_parsers
from miko.parser.parser import Parser


class Function:
    """Retrieves information on a given function"""

    def __init__(self, func: typing.Callable) -> None:
        self.original = func
        self.name = self.original.__name__
        self.signature = inspect.signature(func)
        self.docs = Docs(
            docs=self.original.__doc__ if self.original.__doc__ is not None else "No description",
            signature=self.signature
        )
        self.code = Function.get_code(self.original)
        self.source_filename = self.code.co_filename
        self.source_linenumber = self.code.co_firstlineno
        self.source_name = self.code.co_name
        self.local_variables = self.code.co_names
        self.parameters = self.signature.parameters
        self.return_annotation = self.signature.return_annotation

    @staticmethod
    def get_code(obj: typing.Any) -> types.CodeType:
        """
        Returns the __code__ object of a given callable object.

        Parameters
        ----------
        obj: Callable
            The object to get the __code__ from

        Returns
        -------
        CodeType
            The __code__ object
        """
        if inspect.ismethod(obj):
            obj = obj.__func__
        if inspect.isfunction(obj):
            obj = obj.__code__
        if inspect.istraceback(obj):
            obj = obj.tb_frame
        if inspect.isframe(obj):
            obj = obj.f_code
        if not inspect.iscode(obj):
            raise TypeError('''method, function, traceback, frame,\
                or code object was expected, got {}'''.format(type(obj).__name__))
        return obj

    def __repr__(self) -> str:
        return "<Function '{name}'>".format(name=self.name)


if sys.version_info >= (3, 6):
    SECTIONS_MAP: typing.Dict[str, typing.Type[Parser]] # novermin

SECTIONS_MAP = {
    "PARAMETERS": list_parsers.Parameters,
    "PARAMETER": list_parsers.Parameters,
    "PARAMS": list_parsers.Parameters,
    "PARAM": list_parsers.Parameters,
    "ARGUMENTS": list_parsers.Parameters,
    "ARGUMENT": list_parsers.Parameters,
    "ARGS": list_parsers.Parameters,
    "ARG": list_parsers.Parameters,

    "RETURNS": list_parsers.Returns,
    "RETURN": list_parsers.Returns,
    "RETURNING": list_parsers.Returns,

    "RAISES": list_parsers.Raises,
    "RAISE": list_parsers.Raises,
    "RAISING": list_parsers.Raises,
    "EXCEPTIONS": list_parsers.Raises,
    "EXCEPTION": list_parsers.Raises,
    "ERRORS": list_parsers.Raises,
    "ERROR": list_parsers.Raises,

    "CHANGELOG": list_parsers.Changelog,
    "CHANGES": list_parsers.Changelog,

    "COPYRIGHTS": list_parsers.Copyright,
    "COPYRIGHT": list_parsers.Copyright,
    "AUTHORS": list_parsers.Copyright,
    "AUTHOR": list_parsers.Copyright,

    "EXAMPLES": example_parsers.Example,
    "EXAMPLE": example_parsers.Example
}
"""All of the default sections and their alternative names"""


class Docs:
    """Parses docstrings"""

    def __init__(self,
                 docs: str,
                 signature: typing.Optional[inspect.Signature] = None,
                 noself: bool = False,
                 extra_sections: typing.Optional[typing.Dict[str, typing.Type[Parser]]] = None) -> None:
        sections_map = SECTIONS_MAP.copy()
        sections_map.update(extra_sections or {})

        #  Initializing default values
        self.deprecated = False
        self.parameters = list_parsers.Parameters()
        self.returns = list_parsers.Returns()
        self.raises = list_parsers.Raises()
        self.changelog = list_parsers.Changelog()
        self.copyright = list_parsers.Copyright()
        self.example = example_parsers.Example()
        if sys.version_info >= (3, 6):
            # Always better to have typed attributes
            self.warnings: typing.List[str] = []  # novermin
            self.notes: typing.List[str] = []  # novermin
        else:
            self.warnings = []
            self.notes = []

        self.__elements_mapping__ = {v.__map_attribute__: v for v in (list_parsers.Parameters, list_parsers.Returns,
                                                                      list_parsers.Raises, list_parsers.Changelog,
                                                                      list_parsers.Copyright, example_parsers.Example)}

        if docs is None:
            docs = ""

        self.original = inspect.cleandoc(str(docs))

        if sys.version_info >= (3, 6):
            self.elements: typing.Dict[str, Parser] = {}
        else:
            self.elements = {}

        self.warnings = []
        self.notes = []

        # First, everything is missing
        missing = self.__elements_mapping__.copy()

        description = []

        def clean_name(name: str) -> str:
            """Cleans the string name to normalize it"""
            return name.replace(" ", "").upper().strip()

        for section in self.original.split("\n\n"):
            name, _, body = section.partition("\n---")
            if not body:
                description.append(name)  # name would be the content here
                continue

            # Getting the parser
            parse = sections_map.get(clean_name(name), None)
            if parse is None:
                description.append("\n---".join((name, body)))
                continue

            content = body.lstrip("-").lstrip("\n")
            try:
                self.elements[parse.__map_attribute__].extend(content)
            except Exception:
                self.elements[parse.__map_attribute__] = parse(content, signature=signature, noself=noself)
                missing.pop(parse.__map_attribute__, None)
        self.original_sections = list(self.elements.keys())

        if signature:
            if list_parsers.Parameters.__map_attribute__ not in self.elements:
                self.elements[list_parsers.Parameters.__map_attribute__] = list_parsers.Parameters(signature=signature, noself=noself)
                missing.pop(list_parsers.Parameters.__map_attribute__, None)

            if list_parsers.Returns.__map_attribute__ not in self.elements:
                self.elements[list_parsers.Returns.__map_attribute__] = list_parsers.Returns(signature=signature)
                missing.pop(list_parsers.Returns.__map_attribute__, None)

        for attr, parse in missing.items():
            self.elements[attr] = parse()

        # HANDLING TAGS
        for index, line in enumerate(description):
            start, _, content = str(line).partition(":")
            start = clean_name(start)
            content = content.strip()
            if start in {"WARNING", "WARNINGS"}:
                self.warnings.append(content)
                description[index] = "Warning: {content}".format(content=content)
            elif start in {"NOTE", "NOTES", "SEEALSO", "INFORMATION"}:
                self.notes.append(content)
                description[index] = "Note: {content}".format(content=content)

        if len(description) > 0:
            checking = str(description[0]).replace(" ", "").upper()
            self.deprecated = checking.startswith("!DEPRECATED!") or checking.startswith(
                "!DEPRECATION!") or checking.startswith("!DEPRECATE!") or checking.startswith("!DEPRECATIONNOTICE!")
            if self.deprecated:
                index = description[0].find("!")
                second_index = index + description[0][index + 1:].find("!") + 2
                description[0] = "! DEPRECATED !" + description[0][second_index:]

        self.description = "\n\n".join(description)

    def __repr__(self) -> str:
        return "<Docs sections={sections}>".format(sections=self.original_sections)

    def __getattribute__(self, key: str):
        if key in super().__getattribute__("__elements_mapping__"):
            return self.__getitem__(key)
        return super().__getattribute__(key)

    def __getitem__(self, key: str):
        return self.elements[key]

    def dumps(self, indent=4):
        """Returns a clean docstring"""
        result = ""
        if self.description.replace(" ", ""):
            result += self.description
            result += "\n\n"
        sections = []
        for section in self.elements.values():
            if not isinstance(section, example_parsers.Example) and len(section) <= 0:
                continue

            current_section = ""

            if isinstance(section, example_parsers.Example):
                if not section.original:
                    continue
                current_section += section.__class__.__name__ + "\n"
                current_section += "-" * len(section.__class__.__name__) + "\n"

                current_section += section.original + "\n"
            else:
                current_section += section.__class__.__name__ + "\n"
                current_section += "-" * len(section.__class__.__name__) + "\n"

                for element in section:
                    # element = self.parameters.__element_type__()
                    current_section += element.name

                    if isinstance(element, list_parsers.Parameter):
                        options = []
                        if len(element.types) > 0:
                            options.append(" | ".join([v.__name__ if isinstance(v, type) else str(v) for v in element.types]))
                        if element.default:
                            options.append("default = {default}".format(default=element.default))
                        elif element.optional:
                            options.append("optional")
                        if element.deprecated:
                            options.append("deprecated")

                        if len(options) > 0:
                            current_section += ": " + ", ".join(options)

                    current_section += "\n"

                    for sentence in element.content:
                        current_section += " " * indent + sentence + "\n"

            sections.append(current_section)

        result += "\n".join(sections)

        if result.endswith("\n\n"):
            result = result.removesuffix("\n")

        return result

    def as_dict(self, camelCase: bool = False):
        """Returns the parsed docstring information as a dictionary"""
        results = {
            "description": self.description,
            "notes": self.notes,
            "warnings": self.warnings,
            "deprecated": self.deprecated
        }
        results.update({k: v.as_dict(camelCase) for k, v in self.elements.items()})
        return results
